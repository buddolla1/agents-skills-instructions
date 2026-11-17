# Python Machine Learning Tutorial Notes

Detailed step-by-step notes based on the *Python Machine Learning Tutorial* by Programming with Mosh.

---

## 1. Introduction to Machine Learning

* **Definition:** Machine Learning (ML) is a subset of Artificial Intelligence (AI) where models learn patterns directly from data rather than relying on explicit, traditional rules.
* **Traditional vs. ML Approach:**
  * **Traditional Programming:** You manually code explicit rules for every edge case (e.g., detecting cats vs. dogs based on line/edge detection). This fails when images are black-and-white, rotated, or expanded to new categories.
  * **Machine Learning:** You feed the model thousands of labeled examples (e.g., thousands of pictures of cats and dogs). The algorithm detects underlying patterns automatically and makes predictions on unseen inputs.
* **Common Applications:** Self-driving cars, robotics, natural language processing, computer vision, financial forecasting, and recommendation engines.

---

## 2. High-Level Steps of an ML Project

1. **Import Data:** Load datasets (commonly structured as `.csv` files or database exports).
2. **Clean & Prepare Data:** Remove duplicate rows, drop irrelevant features, handle missing/null values, and encode non-numeric text data (e.g., categories or names) into numerical values.
3. **Split Dataset:** Split the clean data into a **Training set** (typically 70–80%) and a **Test set** (typically 20–30%).
4. **Select & Train Model:** Pick an algorithm (e.g., Decision Trees, Neural Networks) and feed it the training data to learn patterns (`model.fit(X_train, y_train)`).
5. **Predict & Evaluate:** Make predictions on the test set and evaluate model accuracy (`accuracy_score`).
6. **Fine-tune & Iterate:** Tweak hyperparameters or select a different algorithm if the model underperforms.

---

## 3. Core Libraries & Environment Setup

### Key Python Data Science Libraries
* **NumPy:** Handles high-performance multi-dimensional arrays.
* **Pandas:** Provides two-dimensional DataFrames (similar to Excel spreadsheets) for data manipulation and analysis.
* **Matplotlib:** Used for generating 2D plots and data visualizations.
* **Scikit-Learn (sklearn):** Primary library for classical machine learning algorithms, evaluation metrics, and data pre-processing tools.

### Development Environment
* **Jupyter Notebook:** Preferred over standard IDEs (like VS Code or terminals) for data science because it allows cell-by-cell execution, line-by-line inspection, and instant data table rendering.
* **Anaconda Distribution:** Recommended installation method, as it comes pre-packaged with Python, Jupyter Notebook, Pandas, NumPy, and Scikit-Learn.

---

## 4. Basic Data Inspection with Pandas

Using a sample dataset (e.g., Video Game Sales `vgsales.csv`):

```python
import pandas as pd

# Load CSV dataset into a DataFrame
df = pd.read_csv('vgsales.csv')

# Inspect dimensions (rows, columns)
df.shape  # Returns (rows, columns)

# Generate summary statistics for numeric columns
df.describe()  # Returns count, mean, std, min, percentiles, max

# Access underlying 2D NumPy array
df.values
```

---

## 5. Helpful Jupyter Notebook Shortcuts

* **Command Mode (Blue border) vs. Edit Mode (Green border):** Press `Esc` to switch to Command Mode; press `Enter` to edit a cell.
* **`A`**: Insert cell **A**bove.
* **`B`**: Insert cell **B**elow.
* **`D, D`** (double-tap): **D**elete selected cell.
* **`Shift + Tab`**: View inline function docstring / parameters tooltip.
* **`Tab`**: Trigger autocompletion / IntelliSense options.
* **`Ctrl + Enter`**: Run selected cell in place.
* **`Shift + Enter`**: Run selected cell and advance to the next cell.
* **`Cmd/Ctrl + /`**: Toggle line comment.

---

## 6. End-to-End Music Recommendation Example

### Problem Definition
Build a model that predicts what genre of music a new user will like based on their **age** and **gender** ($1 = \text{Male}$, $0 = \text{Female}$).

### Step A: Preparing Features & Labels

Split the dataset into input features ($X$) and output labels ($y$):

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load dataset
music_data = pd.read_csv('music.csv')

# Feature set (Inputs: Age, Gender)
X = music_data.drop(columns=['genre'])

# Label set (Output: Genre)
y = music_data['genre']
```

### Step B: Training & Making Predictions

```python
# Instantiate model
model = DecisionTreeClassifier()

# Train model on inputs and outputs
model.fit(X, y)

# Predict genres for a 21-year-old male (21, 1) and a 22-year-old female (22, 0)
predictions = model.predict([ [21, 1], [22, 0] ])
# Output: array(['Hip-Hop', 'Dance'], dtype=object)
```

### Step C: Evaluating Accuracy

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train on training split
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict on test split
predictions = model.predict(X_test)

# Compare predictions against actual labels
score = accuracy_score(y_test, predictions)
print(score)  # Returns score between 0.0 and 1.0 (75% - 100%)
```

* **Key Takeaway:** Allocating too much data to testing (e.g., `test_size=0.8`) starves the model of training data, significantly degrading accuracy. Larger and cleaner datasets yield more consistent performance.

---

## 7. Model Persistence with Joblib

Training large models on millions of records can take hours. Save the trained model to a file to avoid retraining every time a prediction is made.

```python
import joblib

# 1. Save trained model to disk
joblib.dump(model, 'music-recommender.joblib')

# 2. Load model from disk to make immediate predictions
model = joblib.load('music-recommender.joblib')
predictions = model.predict([[21, 1]])
```

---

## 8. Exporting & Visualizing Decision Trees

Export the decision logic of a trained tree to a visual Graphviz (`.dot`) file:

```python
from sklearn import tree

tree.export_graphviz(
    model,
    out_file='music-recommender.dot',
    feature_names=['age', 'gender'],
    class_names=sorted(y.unique()),
    label='all',
    rounded=True,
    filled=True
)
```

* Open the `.dot` file in VS Code using the **Graphviz (dot) Preview** extension to inspect the decision logic tree visually (e.g., checks like $\text{age} \le 30.5$ followed by $\text{gender} \le 0.5$ to navigate decision branches).