from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model and columns
model = pickle.load(open("crop_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

# Load data to fetch variety and notes
data = pd.read_csv("crop_data_template.csv")

# Clean data
for col in ['Crop', 'Variety', 'Notes']:
    data[col] = data[col].astype(str).str.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input
    season = request.form['season']
    soil = request.form['soil_type']
    water = request.form['water']
    electricity = request.form['electricity']
    maintenance = request.form['maintenance']

    # Create input vector
    input_data = {col: 0 for col in model_columns}
    input_data[f'Season_{season}'] = 1
    input_data[f'Soil_Type_{soil}'] = 1
    input_data[f'Water_{water}'] = 1
    input_data[f'Electricity_{electricity}'] = 1
    input_data[f'Maintenance_{maintenance}'] = 1

    input_df = pd.DataFrame([input_data])

    # Predict
    predicted_label = model.predict(input_df)[0]

    # Get confidence
    probs = model.predict_proba(input_df)[0]
    classes = model.classes_
    confidence = round(probs[list(classes).index(predicted_label)] * 100, 2)

    # Split Crop_Variety
    if "_" in predicted_label:
        predicted_crop, predicted_variety = predicted_label.split("_", 1)
    else:
        predicted_crop = predicted_label
        predicted_variety = "N/A"

    # Match notes
    match = data[
        (data['Crop'].str.lower() == predicted_crop.lower()) &
        (data['Variety'].str.lower() == predicted_variety.lower())
    ]

    if not match.empty:
        notes = match.iloc[0]['Notes']
    else:
        notes = "No notes available."

    # Return output
    return render_template('result.html',
                           prediction=predicted_crop,
                           variety=predicted_variety,
                           confidence=confidence,
                           notes=notes)

if __name__ == '__main__':
    app.run(debug=True)
