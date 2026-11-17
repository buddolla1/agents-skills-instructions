"""OpenObserve log anomaly detection: Isolation Forest + Decision Tree POC.
Install: python3 -m pip install pandas scikit-learn
Demo: python3 log_anomaly_updated.py
OpenObserve: python3 log_anomaly_updated.py logs-data.csv --time-column _timestamp --time-unit us

The tree learns *provisional* Isolation Forest labels, not verified incidents.
Evaluation measures agreement with that detector, not ground-truth accuracy.
"""
import argparse
import random
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

FEATURES = ['total_logs', 'errors', 'db_failures']


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
    return windows.iloc[1:-1]  # Remove potentially partial edge windows.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', nargs='?')
    parser.add_argument('--time-column', default='timestamp')
    parser.add_argument('--message-column', default='log')
    parser.add_argument('--time-unit', choices=['iso', 's', 'ms', 'us', 'ns'], default='iso')
    parser.add_argument('--min-windows', type=int, default=40)
    args = parser.parse_args()
    try:
        if args.csv:
            windows = summarize(pd.read_csv(args.csv), args.time_column,
                                args.message_column, args.time_unit)
        else:
            print('DEMO: synthetic logs with injected spikes.')
            windows = summarize(demo_logs(), 'timestamp', 'log', 'iso')
        if len(windows) < max(args.min_windows, 10):
            raise ValueError(f'Need at least {max(args.min_windows, 10)} interior five-minute windows; several days is preferable.')
        split = int(len(windows) * 0.8)
        train, test = windows.iloc[:split].copy(), windows.iloc[split:].copy()
        if not (train[FEATURES].nunique() > 1).any():
            raise ValueError('Training data is constant; collect representative activity first.')

        # Unsupervised teacher: fit ONLY on earlier windows.
        forest = IsolationForest(n_estimators=200, contamination=0.02, random_state=42)
        forest.fit(train[FEATURES])
        y_train = (forest.predict(train[FEATURES]) == -1).astype(int)
        y_test_teacher = (forest.predict(test[FEATURES]) == -1).astype(int)
        test['isolation_forest_anomaly'] = y_test_teacher.astype(bool)
        test['anomaly_score'] = -forest.decision_function(test[FEATURES])

        # Supervised student: train on provisional labels from the forest.
        # The chronological 80/20 split avoids future data leaking into training.
        tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=3, random_state=42)
        tree.fit(train[FEATURES], y_train)
        predictions = tree.predict(test[FEATURES])
        test['decision_tree_anomaly'] = predictions.astype(bool)
        test['models_agree'] = predictions == y_test_teacher

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test_teacher, predictions, average='binary', zero_division=0)
        print(f'Trained on {len(train)} windows; checked {len(test)} unseen later windows.')
        print('Timestamps are UTC five-minute window starts.')
        print(f'Isolation Forest flagged {int(test.isolation_forest_anomaly.sum())} windows.')
        print(f'Decision Tree flagged {int(test.decision_tree_anomaly.sum())} windows.')
        print('\nDecision Tree agreement with Isolation Forest provisional labels:')
        print(f'Accuracy={accuracy_score(y_test_teacher, predictions):.3f}, '
              f'Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}')
        print('Confusion matrix (rows=forest normal/anomaly; columns=tree normal/anomaly):')
        print(confusion_matrix(y_test_teacher, predictions, labels=[0, 1]))
        flagged = test[test['isolation_forest_anomaly'] | test['decision_tree_anomaly']]
        flagged = flagged.sort_values('anomaly_score', ascending=False)
        print(f'\nFlagged by either model: {len(flagged)} windows.')
        print(flagged.to_string() if len(flagged) else 'No anomalies flagged.')
        print('\nNOTE: Decision Tree labels come from Isolation Forest, NOT confirmed incidents.')
        print('High agreement does not prove accurate incident detection. Review flagged logs manually.')
        print('Empty five-minute buckets are counted as zero; verify ingestion gaps separately.')
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')


if __name__ == '__main__':
    main()
