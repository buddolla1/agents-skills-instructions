"""Local log anomaly detection POC (not an OpenObserve API integration).
Install: python3 -m pip install pandas scikit-learn
Demo: python3 log_anomaly.py
Real CSV: python3 log_anomaly.py logs.csv --time-column _timestamp --time-unit us --message-column log
CSV must contain timestamps and log text for ONE service/environment.
Use --time-unit iso for ISO timestamps (default), or s/ms/us/ns for epoch.
Outputs are printed; no files are overwritten. Use mostly normal history.
"""
import argparse
import random
import pandas as pd
from sklearn.ensemble import IsolationForest


def demo_logs():
    rng = random.Random(42)
    start = pd.Timestamp('2026-11-01', tz='UTC')
    records = []
    for window in range(300):
        count = rng.randint(60, 100)
        errors = rng.randint(0, 4)
        failures = rng.randint(0, 2)
        if window in (260, 280):
            count, errors, failures = 500, 200, 150
        for i in range(count):
            message = ('ERROR database connection failed' if i < failures
                       else 'ERROR request failed' if i < failures + errors
                       else 'INFO request completed')
            records.append({'timestamp': start + pd.Timedelta(minutes=5 * window, seconds=i % 300),
                            'log': message})
    return pd.DataFrame(records)


def summarize(logs, time_column, message_column, time_unit):
    missing = {time_column, message_column} - set(logs.columns)
    if missing:
        raise ValueError(f'Missing CSV columns: {sorted(missing)}')
    values = logs[time_column]
    if time_unit != 'iso':
        values = pd.to_numeric(values, errors='raise')
    timestamps = pd.to_datetime(values, utc=True, errors='raise',
                               **({'unit': time_unit} if time_unit != 'iso' else {}))
    if timestamps.isna().any() or logs[message_column].isna().any():
        raise ValueError('Missing timestamp or message: clean the input first.')
    messages = logs[message_column].astype(str)
    features = pd.DataFrame({
        'total_logs': 1,
        'errors': messages.str.contains(r'\b(?:ERROR|FATAL)\b', case=False, regex=True).astype(int),
        'db_failures': messages.str.contains(
            r'(?:database|mysql|jdbc).*?(?:fail|timeout|refused)|too many connections',
            case=False, regex=True).astype(int),
    })
    features.index = pd.DatetimeIndex(timestamps)
    windows = features.sort_index().resample('5min').sum()
    # Edge buckets may only contain a partial five-minute period.
    # Empty internal buckets remain zero: inspect collection gaps separately.
    return windows.iloc[1:-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', nargs='?')
    parser.add_argument('--time-column', default='timestamp')
    parser.add_argument('--message-column', default='log')
    parser.add_argument('--time-unit', choices=['iso', 's', 'ms', 'us', 'ns'], default='iso')
    args = parser.parse_args()
    try:
        if args.csv:
            windows = summarize(pd.read_csv(args.csv), args.time_column,
                                args.message_column, args.time_unit)
        else:
            print('DEMO: synthetic logs, with injected spikes at 21:40 and 23:20 UTC.')
            windows = summarize(demo_logs(), 'timestamp', 'log', 'iso')
        if len(windows) < 40:
            raise ValueError('Need at least 40 interior five-minute windows; several days is preferable.')
        split = int(len(windows) * 0.8)
        train, test = windows.iloc[:split], windows.iloc[split:].copy()
        if not (train.nunique() > 1).any():
            raise ValueError('Training data is constant; collect representative activity first.')
        model = IsolationForest(n_estimators=200, contamination=0.02, random_state=42)
        model.fit(train)
        test['anomaly'] = model.predict(test) == -1
        # Higher = more unusual; this is NOT a probability.
        test['anomaly_score'] = -model.decision_function(test[train.columns])
        flagged = test[test['anomaly']].sort_values('anomaly_score', ascending=False)
        print(f'Trained on {len(train)} windows; checked {len(test)} unseen later windows.')
        print(f'Flagged {len(flagged)} windows. Window timestamps are UTC start times.')
        print(flagged.to_string() if len(flagged) else 'No anomalies flagged.')
        print('\nPOC: tune message patterns and the 2% training threshold with reviewed real data.')
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')


if __name__ == '__main__':
    main()
