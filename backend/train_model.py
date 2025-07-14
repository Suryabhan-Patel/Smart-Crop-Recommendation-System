import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
df = pd.read_csv("crop_data_template.csv")
print("✅ Dataset loaded")

# Clean crop/variety columns
df['Crop'] = df['Crop'].astype(str).str.strip()
df['Variety'] = df['Variety'].astype(str).str.strip()

# Create target column as "Crop_Variety"
df['CropVariety'] = df['Crop'] + "_" + df['Variety']

# Input features
X = pd.get_dummies(df[['Season', 'Soil_Type', 'Water', 'Electricity', 'Maintenance']])
y = df['CropVariety']

# Save column names
model_columns = X.columns.tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model and features
with open("crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model_columns.pkl", "wb") as f:
    pickle.dump(model_columns, f)

print("✅ Model trained and saved with Crop + Variety target")
