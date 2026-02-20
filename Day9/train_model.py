import csv
import os
import joblib
import util
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# ===============================
# Load Dataset
# ===============================
def load_data(filename="dataset.csv"):
    features = []
    labels = []
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    if not os.path.exists(file_path):
        print("ERROR: dataset.csv not found!")
        return [], []

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract features using util.py
            email_features = util.extract_features(
                row['email'],
                row.get('subject', ''),
                row.get('body', '')
            )
            features.append(email_features)
            labels.append(int(row['label']))

    return features, labels


# ===============================
# Train Model
# ===============================
def train_model(X_train, y_train):
    # Initialize Random Forest Classifier
    # n_estimators=100 means 100 trees, random_state for reproducibility
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model
    clf.fit(X_train, y_train)
    
    return clf


# ===============================
# Evaluate Model
# ===============================
def evaluate_model(model, X_test, y_test):
    # Predict on test data
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print("\n==============================")
    print("MODEL EVALUATION (Random Forest)")
    print("==============================")
    print(f"Accuracy: {accuracy:.2%}")
    print("\nConfusion Matrix:")
    print(f"TP (Spam caught): {tp}")
    print(f"FP (Normal marked as spam): {fp}")
    print(f"TN (Normal correct): {tn}")
    print(f"FN (Spam missed): {fn}")
    
    return accuracy


# ===============================
# Main
# ===============================
if __name__ == "__main__":

    print("=" * 50)
    print("EMAIL SPAM DETECTOR - TRAINING (Random Forest)")
    print("=" * 50)

    # 1. Load Data
    X, y = load_data()

    if not X:
        print("No data found.")
        exit()

    print(f"\nTotal Emails: {len(X)}")

    # 2. Split Data (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training Set: {len(X_train)}")
    print(f"Testing Set: {len(X_test)}")

    # 3. Train Model
    print("\nTraining Random Forest Model...")
    model = train_model(X_train, y_train)

    # 4. Evaluate Model
    evaluate_model(model, X_test, y_test)

    # 5. Save Model
    # We save the model AND the feature names to ensure compatibility
    model_data = {
        "model": model,
        "feature_names": util.get_feature_names()
    }
    
    joblib.dump(model_data, "model.pkl")
    print("\nModel saved as model.pkl")
    print("=" * 50)

