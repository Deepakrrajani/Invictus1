import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv(r"C:\Users\Deepak\OneDrive\Desktop\dataset_edited.csv")

label_encoder = LabelEncoder()
categorical_cols = df.select_dtypes(include=['object']).columns
df[categorical_cols] = df[categorical_cols].apply(label_encoder.fit_transform)

threshold = 5

# Binary target variable
df['at_risk'] = df['G3'] < threshold

# Drop the original target variables G1, G2, G3
df = df.drop(['G1', 'G2', 'G3'], axis=1)

# Specify the columns to include in the feature set X
selected_columns = ['Medu', 'Fedu', 'schoolsup', 'famsup']
X = df[selected_columns]
y = df['underprivileged']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))


import joblib

# Save the trained model to a file
model_filename = 'Classify1.joblib'
joblib.dump(model, model_filename)

print(f"Model saved as {model_filename}")