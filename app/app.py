import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import shap


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
st.write("Predicts whether an FDA adverse event report is likely to be marked serious, "
    "based on drug involvement and report characteristics. This model is trained on real" 
    " data from the FDA Adverse Event Reporting System (FAERS), covering 15 drugs across"
    " several therapeutic categories (pain/NSAID, diabetes, cardiovascular, mental health,"
    " opioid, antibiotic, thyroid). This is a portfolio/demo project, not a clinical "
    " or diagnostic tool.")

#instructions for use
st.write("**How to use this tool:**")
st.write(
    "Enter the details of an adverse event report below:  the drug(s) involved, "
    "the number of reactions and drugs listed, and the patient's sex and age "
    "(or check \"Age unknown\" if unavailable). Click **Predict** to see the model's "
    "estimated likelihood that the report would be marked serious."
)

st.divider()

#group inputs visually
with st.container(border=True):
    #multiselect dropdown list of drugs in a report
    selected_drugs = st.multiselect("Which drugs are involved in this report?",
                                    TARGET_DRUGS, help="Select all drugs mentioned in this" \
                                    " adverse event report.")

    #input # of reactions in a report
    reaction_count = st.number_input("Number of reactions listed", \
                                 min_value=1, max_value=200, value=3,
                                 help="How many distinct reactions/symptoms are listed on this" \
                                 " report.")

    #input # of drugs listed on a report
    drug_count = st.number_input("Number of drugs listed", \
                                 min_value=1, max_value=304, value=3,
                                 help="Total number of drugs mentioned on this report, including " \
                                 "any not in the dropdown above.")

    #select patient sex Unknown/F/M
    sex = st.selectbox("Patient sex", ["Unknown", "Male", "Female"], 
                       help="Patient's sex as reported on the report.")

    #select patient age 

    #if age unknown - use median age:
    age_unknown = st.checkbox("Age unknown", 
                              help="If checked, the model uses the typical (median) " \
                              "patient age from the training data, " \
                              " instead of a specific value.") #returns True or False
    median_age = 62.0

    if age_unknown:
        age = median_age
    else:
        age = st.number_input("Patient age", min_value=0, max_value=110, value=50)

st.divider()

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
    input_scaled = pd.DataFrame(input_scaled, columns=feature_columns)

    #proba of serious cols. (1) at index 0
    probability = model.predict_proba(input_scaled)[:,1][0]

    #apply 0.3 threshold found in modeling notebook
    threshold = 0.30
    prediction = "Serious" if probability >= threshold \
    else "Not Serious"

    #print and explain outcome
    if prediction == "Serious":
        st.error(f"Prediction: {prediction}")
    else:
        st.success(f"Prediction: {prediction}")

    st.metric("Probability of serious outcome", f"{probability:.1%}")

    st.caption(
    "A report is marked 'serious' if it involved an outcome such as "
    "hospitalization, disability or death. This prediction reflects patterns "
    "in historical FAERS reports and does not indicate the real-world risk of "
    "taking any specific drug. FAERS is a voluntary reporting system with no "
    "defined denominator, so incidence rates cannot be calculated from it."
)

    #SHAP explanation for live prediction
    with st.spinner("Computing explanation..."):
        background = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        explainer = shap.Explainer(model, background)
        shap_values = explainer(input_scaled)

    st.write("### Why this prediction?")
    st.write(
    "The chart below shows which factors most influenced this specific prediction. "
    "Each bar represents one input: red bars pushed the prediction toward 'serious', "
    "blue bars pushed it toward 'not serious'. The size of each bar shows how much "
    "that factor mattered for this particular report."
)
    fig = plt.figure()
    shap.plots.waterfall(shap_values[0], show=False)
    st.pyplot(fig)

    st.caption(
    "The number on the left of each bar is that factor's value after standardization "
    "(a technique used to make different types of inputs comparable, so raw numbers "
    "won't match what you entered directly). Drugs you didn't select can still appear "
    "if their absence meaningfully influenced the prediction."
)

