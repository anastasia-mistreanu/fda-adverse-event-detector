import streamlit as st
import pandas as pd
import joblib


TARGET_DRUGS = [
    "Ibuprofen",
    "Aspirin",
    "Acetaminophen",
    "Metformin",
    "Insulin glargine",
    "Atorvastatin",
    "Lisinopril",
    "Warfarin",
    "Apixaban",
    "Sertraline",
    "Alprazolam",
    "Oxycodone",
    "Amoxicillin",
    "Gabapentin",
    "Levothyroxine",
]


model = joblib.load("models/model.joblib")
scaler = joblib.load("models/scaler.joblib")
feature_columns = joblib.load("models/feature_columns.joblib")

#title and desc
st.title("Drug Adverse Event Signal Detector")
st.write("Predict whether an adverse event is likely to be marked serious or not.")

#multiselect dropdown list of drugs in a report
selected_drugs = st.multiselect("Which drugs are involved in this report?", TARGET_DRUGS)

#input # of reactions in a report
reaction_count = st.number_input("Number of reactions listed", \
                             min_value=1, max_value=200, value=3)

#input # of drugs listed on a report
drug_count = st.number_input("Number of drugs listed", \
                             min_value=1, max_value=304, value=3)

#select patient sex Unknown/F/M
sex = st.selectbox("Patient sex", ["Unknown", "Male", "Female"])

#select patient age 

#if age unknown - use median age:
age_unknown = st.checkbox("Age unknown") #returns True or False
median_age = 62.0

if age_unknown:
    age = median_age
else:
    age = st.number_input("Patient age", min_value=0, max_value=110, value=50)


#prediction logic of app

#predict button
if st.button("Predict"):

    #drug flags
    drug_flags = {drug.upper(): (1 if drug in selected_drugs else 0) \
             for drug in TARGET_DRUGS}

    #patient sex flags
    sex_code_map = {"Unknown": "0", "Male": "1", "Female": "2"}
    selected_code = sex_code_map[sex] #based on drop-down box 

    sex_flags = {
        "patientsex_0": 1 if selected_code == "0" else 0,
        "patientsex_1": 1 if selected_code == "1" else 0,
        "patientsex_2": 1 if selected_code == "2" else 0,
    }


    #collect all input data in one dict
    input_data = {
        "reaction_count": reaction_count,
        "drug_count": drug_count,
        "patientonsetage_years": age
    }
    #add flags to input_data too
    input_data.update(drug_flags)
    input_data.update(sex_flags)


    #build dataframe for scikit learn for training model 
    #from input data
    input_df = pd.DataFrame([input_data])
    input_df =input_df[feature_columns]

    #scaling input as per model
    input_scaled = scaler.transform(input_df)
    #proba of serious cols. (1) at index 0
    probability = model.predict_proba(input_scaled)[:,1][0]

    #apply 0.3 threshold found in modeling notebook
    threshold = 0.30
    prediction = "Serious" if probability >= threshold \
    else "Not Serious"

    #print outcome on app
    st.write(f"### Prediction: {prediction}")
    st.write(f"Predicted probability of serious outcome {probability: .2%}")
    