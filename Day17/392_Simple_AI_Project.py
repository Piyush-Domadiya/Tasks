#Choose a dataset (e.g., Titanic, MNIST) and build a complete machine learning pipeline.


# 1. Import Libraries


import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score,StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# 2. Load Dataset

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)


# Basic Cleaning
df.drop_duplicates(inplace=True)
df.drop(['PassengerId','Name','Ticket','Cabin'], axis=1, inplace=True)

# Feature Engineering
df['FamilySize'] = df['SibSp'] + df['Parch']
df['IsAlone'] = (df['FamilySize'] == 0).astype(int)



df.to_csv("titanic.csv", index=False)
df.isnull().sum()
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')

#df = pd.read_csv("titanic.csv")


# 3. Select Features & Target

df['FamilySize'] = df['SibSp'] + df['Parch']
df['IsAlone'] = (df['FamilySize'] == 0).astype(int)
X = df[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','FamilySize','IsAlone']]
y = df['Survived']


# 4. Define Column Types


numeric_features = ['Age','Fare','FamilySize','IsAlone']
categorical_features = ['Pclass','Sex','Embarked']


# 5. Preprocessing Pipelines


numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combine both
preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('cat', categorical_pipeline, categorical_features)
])


# 6. Full Pipeline (Preprocessing + Model)


pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    class_weight='balanced',
    random_state=42 ))
])


# 7. Train-Test Split


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y   
)


# 8. Train Model


pipeline.fit(X_train, y_train)


# 9. Predictions

y_pred_class = pipeline.predict(X_test)        # For Accuracy
y_pred_proba = pipeline.predict_proba(X_test)[:,1]  # For ROC-AUC


# 10. Evaluation


print("Accuracy:", accuracy_score(y_test, y_pred_class))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_class))
print("\nClassification Report:\n", classification_report(y_test, y_pred_class))
print("\nROC AUC Score:", roc_auc_score(y_test, y_pred_proba))


# 11. Cross Validation


cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring='roc_auc')
print("\nCross Validation ROC AUC:", np.mean(cv_scores))


# 12. Save Model


joblib.dump(pipeline, "titanic_pipeline_model.pkl")

print("\nModel saved successfully!")