import streamlit as st
import pandas as pd
import numpy as np
import joblib  

# Load the trained model
model = joblib.load('cred_risk_best_model.pkl')  

# Define the manual mapping for credit score categories
loan_score_mapping = {0: 'Paid', 1: 'Default'}

home_ownership_mappings = {'MORTGAGE': 0, 'OTHER': 1, 'OWN': 2, 'RENT': 3}

loan_reason_mappings =  {'DEBT CONSOLIDATION': 0, 
                         'EDUCATION': 1, 
                         'HOME IMPROVEMENT': 2, 
                         'MEDICAL': 3, 
                         'PERSONAL': 4, 
                         'VENTURE': 5}


loan_grade_mappings = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}

historical_default_mappings = {'N': 0, 'Y': 1}
default_mappings = {'No Default': 0, 'Default': 1}

# Reverse mappings for dropdowns
loan_reasons = list(loan_reason_mappings.keys())
home_ownership_options = list(home_ownership_mappings.keys())
loan_grades = list(loan_grade_mappings.keys())

# Streamlit App
st.title("Default Prediction")

# Collect user inputs for features
try:
    Age = int(st.text_input("Age (in years)", "30"))
    Income = float(st.text_input("Income", "50000"))
    Home_own = st.selectbox("Home Ownership", home_ownership_options)
    Emp_len = int(st.text_input("Years Employed", "2"))
    Loan_intent = st.selectbox("Reason for Loan", loan_reasons)
    Loan_grd = st.selectbox("Loan Grade", loan_grades)
    Amount = float(st.text_input("Loan Amount", "5000"))
    Int_rate = float(st.text_input("Loan Interest Rate", "12.6"))
    Loan_percent_Inc = float(st.text_input("Loan % of Income", f"{round(Amount / Income, 4)}"))
    Hist_def = st.selectbox("Historical Default", ["No", "Yes"])
    Cred_Hist_Len = float(st.text_input("Credit History Length (years)", "5.5"))

    # Encode categorical inputs
    encoded_home_own = home_ownership_mappings[Home_own]
    encoded_reasons = loan_reason_mappings[Loan_intent]
    encoded_grade = loan_grade_mappings[Loan_grd]
    encoded_hist_def = 0 if Hist_def == "No" else 1

    if st.button("Predict Default"):
        # Create a DataFrame for the input
        input_data = pd.DataFrame({
            'person_age': [Age],
            'person_income': [Income],
            'person_home_ownership': [encoded_home_own],
            'person_emp_length': [Emp_len],
            'loan_intent': [encoded_reasons],
            'loan_grade': [encoded_grade],
            'loan_amnt': [Amount],
            'loan_int_rate': [Int_rate],
            'loan_percent_income': [Loan_percent_Inc],
            'cb_person_default_on_file': [encoded_hist_def],
            'cb_person_cred_hist_length': [Cred_Hist_Len]    
        })

        # Predict using the model
        predicted_score = model.predict(input_data)[0]

        # Map the prediction to the category
        prediction_category = loan_score_mapping[predicted_score]

        if predicted_score == 0:
            st.success(f"The Default prediction result is: {prediction_category}")
        elif predicted_score == 1:
            st.markdown(f"<p style='color:red; font-weight:bold;'>The Default prediction result is: {prediction_category}</p>", 
        unsafe_allow_html=True
    )

except ValueError:
    st.error("Please ensure all numeric inputs are valid numbers.")