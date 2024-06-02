import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import xgboost as xgb
import matplotlib.pyplot as plt

# Load the trained model and label encoders
model = xgb.XGBClassifier()
model.load_model('xgboost_model.json')
with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

# Define the parameters for the input form
params = ['NO OF CHEMO CYCLE', 'CA COLON STAGE', 'AGE', 'SEX', 'HB % gms', 'TWBC cells/cu.mm', 'PC/Lakhs/cumm', 'S.CR mgs/dl', 'S.T.BILIRUBIN mgs/dl', 'S.CEA ng/mL']

# Function to save data
def save_data(mri_number, data):
    # Check if the general CSV file exists
    if not os.path.isfile('patient_data.csv'):
        # Create a new CSV file
        df = pd.DataFrame(columns=['MRI_NUMBER'] + params)
        df.to_csv('patient_data.csv', index=False)

    # Append new data to the general CSV file
    df = pd.read_csv('patient_data.csv')
    new_data = pd.DataFrame([{'MRI_NUMBER': mri_number, **data}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv('patient_data.csv', index=False)

    # Save data separately for each MRI number
    filename = f'{mri_number}.csv'
    if not os.path.isfile(filename):
        pd.DataFrame(columns=params).to_csv(filename, index=False)
    df = pd.read_csv(filename)
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(filename, index=False)

# Function to load data for prediction
def load_data(mri_number):
    filename = f'{mri_number}.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return None

# Streamlit UI
st.title('ChemoCure Application')

menu = ['Data Upload', 'Prediction']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Data Upload':
    st.subheader('Data Upload')
    
    mri_number = st.text_input('Enter 5-digit MRI number')
    
    if len(mri_number) == 5:
        data = {}
        for param in params:
            data[param] = st.text_input(f'Enter {param}')
        
        if st.button('Save Data'):
            save_data(mri_number, data)
            st.success('Data saved successfully')
    else:
        st.warning('Please enter a valid 5-digit MRI number')

elif choice == 'Prediction':
    st.subheader('Prediction')
    
    mri_number = st.text_input('Enter 5-digit MRI number for prediction')
    
    if st.button('Predict'):
        df = load_data(mri_number)
        if df is not None:
            if len(df) > 1:
                st.write('Patient Data:')
                st.write(df)
                
                # Graphs for hematological parameters
                st.write('Hematological Parameters:')
                hemat_params = ['HB % gms', 'TWBC cells/cu.mm', 'PC/Lakhs/cumm', 'S.CR mgs/dl', 'S.T.BILIRUBIN mgs/dl', 'S.CEA ng/mL']
                for param in hemat_params:
                    st.write(f"**{param}**")
                    st.line_chart(df[param])
                
                # Prepare data for prediction
                df_processed = df.copy()
                for column in df_processed.columns:
                    if column in label_encoders:
                        le = label_encoders[column]
                        df_processed[column] = le.transform(df_processed[column])
                    df_processed[column] = pd.to_numeric(df_processed[column], errors='coerce')
                
                X = df_processed[params]
                predictions = model.predict(X)
                
                # Show predictions
                df['Prediction'] = label_encoders['Observation'].inverse_transform(predictions)
                st.write('Predictions:')
                st.write(df[['NO OF CHEMO CYCLE', 'Prediction']])
                
                # Check for improvement or needed improvement
                improvement_status = 'Improvement' if all(df['Prediction'] == 'Improvement') else 'Needed Improvement'
                st.write(f'Suggestion: {improvement_status}')
            else:
                st.warning('Please upload data for more than one chemo cycle to make predictions and comparisons.')
        else:
            st.error('MRI number not found in the database')

# To run the Streamlit app, save this script as 'app.py' and run 'streamlit run app.py' in the terminal.
