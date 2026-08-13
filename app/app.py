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
rxn_count = st.number_input("Number of reactions listed", \
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

