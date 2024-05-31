import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define patient records
data = {
    '12345': {
        'HB % gms': [12.5, 11.5, 10.4, 10.5, 11.6, 11.8, 12, 12.5],
        'TWBC cells/cu.mm': [12760, 5720, 4120, 5740, 3770, 4350, 4730, 5630],
        'PC/Lakhs/cumm': [2.6, 2.04, 0.75, 1.2, 0.85, 1.21, 1.52, 2],
        'S.CR mgs/dl': [0.9, 0.4, 0.5, 0.6, 0.5, 0.6, 0.8, 0.8],
        'S.T.BILIRUBIN mgs/dl': [2.5, 0.8, 1.9, 1.7, 1.7, 1.4, 1.2, 1],
        'S.CEA ng/mL': [11.06, 10.05, 9.01, 8.77, 8.02, 7.99, 7.54, 6.55]
    }
}

# Streamlit app
st.title("Patient Medical Records")

# Input field for MRN
mrn = st.text_input("Enter Medical Record Number (5 digit)")

if mrn:
    if mrn in data:
        st.subheader(f"Patient {mrn} Records")
        df = pd.DataFrame(data[mrn])
        st.write(df)

        st.subheader("Graphs")
        for parameter in df.columns:
            plt.plot(df.index, df[parameter], marker='o', label=parameter)
            plt.xlabel("Chemotherapy Sessions")
            plt.ylabel(parameter)
            plt.title(f"{parameter} Variation over Chemotherapy Sessions")
            plt.xticks(range(len(df.index)), ['Baseline', 'Before III', 'Before V', 'After VII', 'After 9 months', 'After 12 months', 'After 15 months', 'After 18 months'], rotation=45)
            plt.legend()
            st.pyplot(plt)
    else:
        st.error("Patient not found!")
