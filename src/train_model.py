import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
from drugs import TARGET_DRUGS

def main():
    conn = sqlite3.connect("data/fda_adverse_events.db")
    df = load_and_clean_data(conn)
    ...

def load_and_clean_data(conn):
    #import reports table
    df = pd.read_sql_query("SELECT * FROM reports", conn)

    #fill missing patientonsetage_years w/ median
    df["patientonsetage_years"] = df["patientonsetage_years"].fillna(df["patientonsetage_years"].median())

    #fill patientsex null values with 0
    df["patientsex"] = df["patientsex"].fillna("0")

    return df


def build_drug_features(conn):
    #get ID and raw drug name (medicinalproduct) for each drug
    drug_join_df = pd.read_sql_query("SELECT safetyreportid, medicinalproduct " \
                                    "FROM drugs", conn)


    #conv. drug names to Ucase to match case-insensitively
    drug_join_df["drug_upper"] = drug_join_df["medicinalproduct"].str.upper()
    target_upper = [d.upper() for d in TARGET_DRUGS] #list comprehension
    pattern = "|".join(target_upper) #combine drugs into "OR" regex to match Ucase drugs


    #keep rows where raw drug name contains at least 1 target drug inside it
    filtered_drugs_df = drug_join_df[drug_join_df["drug_upper"].str.contains(\
        pattern, na=False)]

    #change messy drug names into clean drug names
    filtered_drugs_df["clean_drug"] = filtered_drugs_df[\
        "drug_upper"].apply(find_target_drug, args=(target_upper,))


    #one row per report, one col. per clean drug name + counts
    drug_features_df = pd.crosstab(filtered_drugs_df["safetyreportid"], \
                                   filtered_drugs_df["clean_drug"])

    #cap cells at 1 for binary classification (y/n)
    drug_features_df = drug_features_df.clip(upper=1) 

    #safetyreportid reverted from index
    drug_features_df = drug_features_df.reset_index()

    return drug_features_df


def find_target_drug(drug_name, target_list):
    #loops through each 15 target drug (Ucase)
    for drug in target_list:   #check if target drug appears in raw drug_name str
        if drug in drug_name:  #finds match, returns clean target drug name
            return drug
        
    return None #no match, return None


def build_features(df, drug_features_df):
    ...


def train_and_save_model(X, y):
    ...


if __name__ == "__main__":
    main()