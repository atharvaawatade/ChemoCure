import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import xgboost as xgb
import pickle

# Load the data
df = pd.read_csv('patient_data.csv')

# Print the column names to verify
print("Columns in the DataFrame:", df.columns)

# Preprocess the data
# Fill any missing values using forward fill method
df.ffill(inplace=True)

# Convert necessary columns to appropriate numeric types
# List the columns that should be numeric
numeric_columns = ['NO OF CHEMO CYCLE', 'CA COLON STAGE', 'AGE', 'HB % gms',
                   'TWBC cells/cu.mm', 'PC/Lakhs/cumm', 'S.CR mgs/dl',
                   'S.T.BILIRUBIN mgs/dl', 'S.CEA ng/mL']

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Encode categorical variables
label_encoders = {}
for column in ['SEX']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Split the data into features (X) and target (y)
X = df.drop(columns=['Observation', 'S.NO'])
y = df['Observation']

# Encode the target column 'Observation'
observation_encoder = LabelEncoder()
y = observation_encoder.fit_transform(y)
label_encoders['Observation'] = observation_encoder

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a machine learning model (e.g., XGBoost) with categorical feature support
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', enable_categorical=True)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the label encoders and model for future use
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
model.save_model('xgboost_model.json')
