# OpenObserve Log Anomaly Detection — Step-by-Step Notes

## 1. Goal and architecture

This guide documents the uploaded `log_anomaly_decision_tree.py` program, which analyzes exported OpenObserve CSV logs locally on a Mac. It is **not** a live OpenObserve API integration.

**Flow:** OpenObserve logs → export CSV → Pandas parses timestamps and messages → aggregate five-minute windows → Isolation Forest identifies unusual windows → Decision Tree learns *provisional* labels from Isolation Forest → evaluate on later windows → save model with Joblib → export tree as Graphviz DOT → optionally reload the saved tree to predict on a new CSV.

The Decision Tree does **not** learn verified production incidents unless the training labels are later replaced with reviewed ground truth. Its accuracy and recall here measure agreement with Isolation Forest.

## 2. Files and prerequisites

Keep these in your working folder:

- `log_anomaly_decision_tree.py` — Python program.
- `logs-data.csv` — CSV exported from OpenObserve.
- `log-anomaly-decision-tree.joblib` — trained Decision Tree, created by training.
- `log-anomaly-decision-tree.dot` — tree visualization source, created by training.
- `decision-tree.png` — optional image rendered from the DOT file.

Your previously observed OpenObserve CSV header was:

```csv
_timestamp,container_id,container_name,log,source,_stream_name,stream_prefix
```

The program uses `_timestamp` and `log`; the other columns are not currently model features. Export logs for one service/environment when possible to avoid mixing unrelated activity.

## 3. Open Terminal and check your files

```bash
cd /path/to/your/project
pwd
ls -lh
python3 --version
```

Replace `/path/to/your/project` with the folder containing the Python script and CSV. `pwd` shows the current directory; `ls -lh` shows files and sizes.

## 4. Create an isolated Python environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install pandas scikit-learn joblib
```

Pandas loads and aggregates logs; scikit-learn provides Isolation Forest, Decision Tree, and evaluation metrics; Joblib saves and loads trained models.

Check packages:

```bash
python3 -m pip show pandas scikit-learn joblib
```

## 5. Verify the CSV before training

```bash
head -n 2 logs-data.csv
wc -l logs-data.csv
```

The first command shows the header and one data row. The second counts CSV lines (approximately records + header; embedded newlines can affect the count). Check whether `_timestamp` contains numeric Unix microseconds or ISO-formatted date/time strings.

**Numeric microseconds example:** `1794610800000000` → use `--time-unit us`.

**ISO example:** `2026-11-13T19:00:00Z` → use `--time-unit iso`.

Other supported units are `s`, `ms`, and `ns`. Choosing the wrong unit can produce invalid or misleading dates.

## 6. Run the built-in demo first

```bash
python3 log_anomaly_decision_tree.py
```

Without a CSV argument, the script generates synthetic logs, including deliberately injected spikes. This checks the end-to-end training and export flow without needing OpenObserve.

## 7. Export real logs from OpenObserve

1. Open OpenObserve and navigate to **Logs**.
2. Select the appropriate stream, such as the MySQL container log stream.
3. Choose a time range containing enough **actual** collected history; 24 hours or several days is preferable.
4. Run the query and inspect the results.
5. Use **Download to CSV** and save the file as `logs-data.csv` in the working directory.
6. Check that the export contains the full intended time range and is not restricted to a small result-page limit.

Selecting “Last 24 hours” does not create 24 hours of data if ingestion started recently.

## 8. Train with real OpenObserve CSV

For the observed `_timestamp` and `log` columns, assuming numeric microsecond timestamps:

```bash
python3 log_anomaly_decision_tree.py logs-data.csv \
  --time-column _timestamp \
  --message-column log \
  --time-unit us
```

For ISO timestamps, replace `us` with `iso`.

**What the script does:**

1. Loads the CSV using `pd.read_csv()`.
2. Validates the timestamp and message column names.
3. Converts timestamps to UTC.
4. Counts total logs, `ERROR`/`FATAL` messages, and database-failure patterns in each five-minute bucket.
5. Removes the first and last buckets because they may be partial.
6. Requires at least **40 interior five-minute windows** by default, and nonconstant training features.
7. Splits windows chronologically: first 80% for training and last 20% for testing.
8. Fits `IsolationForest(n_estimators=200, contamination=0.02, random_state=42)` on training windows only.
9. Creates provisional anomaly labels from Isolation Forest predictions.
10. Fits `DecisionTreeClassifier(max_depth=4, min_samples_leaf=3, random_state=42)` on the training features and provisional labels.
11. Evaluates both models on later test windows and prints a confusion matrix and agreement metrics.
12. Saves the Decision Tree with Joblib and exports the tree to Graphviz DOT.

**Features:**

| Feature | Meaning |
|---|---|
| `total_logs` | Number of log messages in a five-minute window |
| `errors` | Messages matching `ERROR` or `FATAL` |
| `db_failures` | Messages matching the script's database/MySQL/JDBC failure patterns |

The script's anomaly score is **not a probability**. Positive/negative score interpretation follows its `-forest.decision_function(...)` calculation; larger values indicate more unusual behavior under that model.

## 9. Save the model and understand the outputs

Training creates these files by default:

```text
log-anomaly-decision-tree.joblib
log-anomaly-decision-tree.dot
```

To choose custom filenames:

```bash
python3 log_anomaly_decision_tree.py logs-data.csv \
  --time-column _timestamp --message-column log --time-unit us \
  --model-out mysql-anomaly-tree.joblib \
  --tree-dot mysql-anomaly-tree.dot
```

The `.joblib` bundle includes the fitted Decision Tree, ordered feature names, label source, and five-minute window metadata. **Only load Joblib files from trusted sources:** loading a malicious serialized file can execute code.

## 10. Render the Decision Tree as an image on macOS

Install Graphviz once (requires Homebrew):

```bash
brew install graphviz
```

Convert the generated DOT file into a PNG:

```bash
dot -Tpng log-anomaly-decision-tree.dot -o decision-tree.png
open decision-tree.png
```

Or export a scalable vector image:

```bash
dot -Tsvg log-anomaly-decision-tree.dot -o decision-tree.svg
open decision-tree.svg
```

The tree diagram shows splits using `total_logs`, `errors`, and `db_failures`; leaf labels are `Normal` and `Anomaly`. It reflects learned *provisional* labels, not confirmed root causes.

## 11. Load a previously saved model to predict on new logs

Export a **new** CSV (example `logs-next-day.csv`) and run:

```bash
python3 log_anomaly_decision_tree.py logs-next-day.csv \
  --time-column _timestamp \
  --message-column log \
  --time-unit us \
  --predict-model log-anomaly-decision-tree.joblib
```

This loads the saved **Decision Tree** and predicts for the new CSV's five-minute windows. It **does not retrain** and **does not run Isolation Forest** in prediction-only mode. Predictions are printed to Terminal; the script does not write a predictions CSV.

The model expects the same feature definitions and five-minute aggregation. If log formats, message patterns, or application behavior change, retraining and validation may be needed.

## 12. Interpret evaluation output

| Output | Interpretation |
|---|---|
| `Trained on ... windows` | Earlier windows used for training |
| `checked ... unseen later windows` | Later windows used for testing |
| `Isolation Forest flagged` | Unusual windows according to Isolation Forest |
| `Decision Tree flagged` | Windows predicted anomalous by the classifier |
| `Accuracy` | Overall agreement with provisional Isolation Forest labels |
| `Precision` | Of tree anomaly predictions, fraction also flagged by forest |
| `Recall` | Of forest anomalies, fraction detected by tree |
| `F1` | Harmonic mean of precision and recall |
| `Confusion matrix` | Rows = forest normal/anomaly; columns = tree normal/anomaly |
| `Flagged by either model` | Union of both models' flagged test windows |

**Important:** High accuracy can be misleading when anomalies are rare. A tree predicting all windows as normal can still have high overall agreement and zero anomaly recall. Manually inspect flagged raw logs before calling them incidents.

## 13. Common errors and fixes

### `No such file or directory`

```bash
pwd
ls -lh
```

Check the script and CSV filenames and working directory. If the script is in the current folder, use `python3 log_anomaly_decision_tree.py ...`.

### `Missing CSV columns: ['timestamp']`

Your OpenObserve export uses `_timestamp`, not `timestamp`. Add:

```bash
--time-column _timestamp
```

### Timestamp parsing fails

Inspect the first data row:

```bash
head -n 2 logs-data.csv
```

Use the matching `--time-unit`: `us` for microseconds, `ms` for milliseconds, `s` for seconds, or `iso` for formatted timestamps.

### `Need at least 40 interior five-minute windows`

Collect and export more actual log history. Forty complete five-minute windows correspond to at least 200 minutes of interior windows, plus possible partial edge buckets. **Several days are preferable** for a representative baseline. The script has a `--min-windows` option for experiments, but reducing it does not improve model reliability.

### `Training data is constant`

Training windows show no meaningful variation. Collect representative traffic and verify log ingestion and parsing.

### `No module named ...`

Activate the environment and reinstall dependencies:

```bash
source .venv/bin/activate
python3 -m pip install pandas scikit-learn joblib
```

### Graphviz `dot: command not found`

```bash
brew install graphviz
dot -V
```

### Model flags no anomalies

This does not prove the system is healthy. The Decision Tree may have learned too few positive examples. Check Isolation Forest output, test-period coverage, and manually reviewed examples.

## 14. Command-line options reference

```bash
python3 log_anomaly_decision_tree.py --help
```

| Option | Default | Purpose |
|---|---|---|
| Positional `csv` | None | CSV path; omit for synthetic demo |
| `--time-column` | `timestamp` | Timestamp field |
| `--message-column` | `log` | Log text field |
| `--time-unit` | `iso` | Timestamp representation (`iso`, `s`, `ms`, `us`, `ns`) |
| `--min-windows` | `40` | Minimum interior windows for training; floor of 10 |
| `--model-out` | `log-anomaly-decision-tree.joblib` | Saved Decision Tree path |
| `--predict-model` | None | Load saved tree for prediction-only mode |
| `--tree-dot` | `log-anomaly-decision-tree.dot` | DOT visualization path |

## 15. Recommended next improvements

1. **Ground-truth labels:** Review real incidents and label anomalous windows; train a classifier against those labels instead of only Isolation Forest output.
2. **Better features:** Add error rate, database timeout count, exception types, and service/container grouping when supported by the exported logs.
3. **Data quality:** Distinguish zero-traffic windows from missing ingestion; current script fills empty internal five-minute buckets with zeros.
4. **Model monitoring:** Track precision/recall on verified incidents, false positives, and changes in production traffic patterns.
5. **Automation:** Once the CSV workflow is validated, consider OpenObserve API ingestion and scheduled prediction as a separate enhancement.

## 16. Quick copy/paste command sequence

```bash
# From the folder containing your Python script and exported CSV
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pandas scikit-learn joblib

# Inspect the CSV
head -n 2 logs-data.csv

# Train, evaluate, save Joblib, and export Graphviz DOT
python3 log_anomaly_decision_tree.py logs-data.csv \
  --time-column _timestamp --message-column log --time-unit us

# Optional: visualize the tree
brew install graphviz
dot -Tpng log-anomaly-decision-tree.dot -o decision-tree.png
open decision-tree.png

# Later: predict using a fresh exported CSV
python3 log_anomaly_decision_tree.py logs-next-day.csv \
  --time-column _timestamp --message-column log --time-unit us \
  --predict-model log-anomaly-decision-tree.joblib
```

> These commands assume `_timestamp` contains Unix microseconds. Verify the timestamp format first and use `--time-unit iso` if the CSV contains ISO timestamps.
