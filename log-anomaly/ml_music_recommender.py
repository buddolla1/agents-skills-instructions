import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def main():
    # 1. Load the dataset
    # (Ensure 'music.csv' is in the same directory as this script)
    try:
        music_data = pd.read_csv('music.csv')
    except FileNotFoundError:
        print("Error: 'music.csv' file not found. Please place it in the working directory.")
        return

    print("--- Dataset Loaded Successfully ---")
    print(music_data.head(), "\n")

    # 2. Clean and Split Data into Features (X) and Labels (y)
    # X contains input features: age and gender
    X = music_data.drop(columns=['genre'])
    # y contains the target output: genre
    y = music_data['genre']

    # 3. Split the data into Training (80%) and Testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # 4. Instantiate and Train the Decision Tree Model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # 5. Evaluate Model Accuracy using the Test Set
    predictions = model.predict(X_test)
    score = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {score * 100:.2f}%\n")

    # 6. Make Predictions for New Users
    # Format: [ [age, gender] ] where gender: 1 = Male, 0 = Female
    sample_users = [
        [21, 1],  # 21-year-old male
        [22, 0]   # 22-year-old female
    ]
    new_predictions = model.predict(sample_users)
    print("Predictions for new users:")
    for user, genre in zip(sample_users, new_predictions):
        print(f"Age: {user[0]}, Gender: {'Male' if user[1] == 1 else 'Female'} -> Recommended Genre: {genre}")

    # 7. Model Persistence: Save the trained model to disk
    model_filename = 'music-recommender.joblib'
    joblib.dump(model, model_filename)
    print(f"\nTrained model successfully saved to '{model_filename}'!")

    # --- Example of Loading and Using the Saved Model Later ---
    # loaded_model = joblib.load(model_filename)
    # saved_predictions = loaded_model.predict([[25, 1]])
    # print(f"Loaded model prediction for 25-year-old male: {saved_predictions[0]}")

if __name__ == "__main__":
    main()