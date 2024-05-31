import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the CSV file path
csv_file_path = 'patient_data.csv'

# Ensure the CSV file exists with headers if it does not exist
if not os.path.exists(csv_file_path):
    # Create the CSV file with appropriate columns if it does not exist
    df_init = pd.DataFrame(columns=['MRN', 'Session', 'HB % gms', 'TWBC cells/cu.mm', 'PC/Lakhs/cumm', 'S.CR mgs/dl', 'S.T.BILIRUBIN mgs/dl', 'S.CEA ng/mL'])
    df_init.to_csv(csv_file_path, index=False)

# Streamlit app
st.title("Patient Medical Records")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["View Records", "Enter Data"])

if menu == "View Records":
    # Input field for MRN
    mrn = st.text_input("Enter Medical Record Number (5 digit)")

    if mrn:
        try:
            df = pd.read_csv(csv_file_path, dtype={'MRN': str})  # Ensure MRN is read as a string
            st.write("Loaded data from CSV:", df)  # Debug: Show loaded data

            patient_data = df[df['MRN'] == mrn]
            st.write(f"Filtered data for MRN {mrn}:", patient_data)  # Debug: Show filtered data

            if not patient_data.empty:
                st.subheader(f"Patient {mrn} Records")
                st.write(patient_data)

                st.subheader("Graphs")
                sessions = patient_data['Session'].unique()
                for parameter in patient_data.columns[2:]:
                    plt.figure()
                    plt.plot(sessions, patient_data[parameter], marker='o')
                    plt.xlabel("Sessions")
                    plt.ylabel(parameter)
                    plt.title(f"{parameter} Variation over Sessions")
                    plt.xticks(rotation=45)
                    st.pyplot(plt)
            else:
                st.error("Patient not found!")
        except pd.errors.EmptyDataError:
            st.error("No data available!")

elif menu == "Enter Data":
    st.subheader("Enter Patient Data")
    
    # Input fields for MRN and patient data
    mrn = st.text_input("Enter Medical Record Number (5 digit)")

    sessions = [
        "Baseline", "Before III chemo", "Before V chemo", 
        "After VII chemo", "After 9 months", "After 12 months", 
        "After 15 months", "After 18 months"
    ]

    data = {'MRN': [], 'Session': sessions}
    
    if mrn:
        for session in sessions:
            data['MRN'].append(mrn)
        
        for parameter in ['HB % gms', 'TWBC cells/cu.mm', 'PC/Lakhs/cumm', 'S.CR mgs/dl', 'S.T.BILIRUBIN mgs/dl', 'S.CEA ng/mL']:
            values = []
            for session in sessions:
                value = st.number_input(f"{parameter} ({session})", step=0.01)
                values.append(value)
            data[parameter] = values

        # Button to save data
        if st.button("Save Data"):
            df_new = pd.DataFrame(data)
            if os.path.exists(csv_file_path):
                df_existing = pd.read_csv(csv_file_path, dtype={'MRN': str})
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(csv_file_path, index=False)
                st.write("Updated CSV Data:", df_combined)  # Debug: Show updated CSV data
            else:
                df_new.to_csv(csv_file_path, index=False)
            st.success(f"Data for patient {mrn} has been saved successfully!")
