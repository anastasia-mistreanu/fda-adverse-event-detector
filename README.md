# fda-adverse-event-detector
# Drug Adverse Event Signal Detector

Predicting whether a drug adverse event report is likely to be marked serious, using real FDA safety data.

**Live demo:** https://fda-adverse-event-detector.streamlit.app/

## Overview

This project builds a full pipeline, from raw regulatory data to a deployed, explainable prediction tool, using real reports from the FDA Adverse Event Reporting System (FAERS). FAERS supports the FDA's post-marketing drug safety surveillance program and contains adverse event and medication error reports submitted by manufacturers, healthcare professionals, and consumers [1, 2].

The dataset covers 23,173 unique reports across 15 target drugs spanning several therapeutic categories: pain/NSAID, diabetes, cardiovascular, mental health, opioid, antibiotic and thyroid.

FAERS is a voluntary, spontaneous reporting system. FDA states directly that the presence of a report does not mean the reported product caused the event [6], and the database has no defined denominator, so incidence rates cannot be calculated from it [8]. This project treats the data accordingly: predictions describe patterns in historical reporting, not real world drug risk. Full reasoning and citations are in `notebooks/eda.ipynb` and `fda_references.md`.

## Pipeline

1. **Fetch**: pull adverse event reports from the openFDA drug/event API, one search per target drug, with pagination and error handling
2. **Deduplicate and store**: since a single report can mention multiple target drugs, it can be returned by more than one search. Reports are deduplicated and stored in a three table relational database (`reports`, `drugs`, `reactions`) reflecting the real one to many structure of the data
3. **Feature engineer**: SQL based features (reaction count, drug count per report) plus a fix for a real data quality bug (patient age recorded in mixed units, corrected to a consistent `patientonsetage_years` field)
4. **EDA**: full exploratory analysis, including a drug level comparison of serious report rates, all findings cited against peer reviewed and official sources
5. **Model**: logistic regression predicting whether a report is serious, with a documented path from a naive failing baseline to a tuned, feature rich final model
6. **Explain**: SHAP explainability, both in the modeling notebook and live in the demo app
7. **Deploy**: a Streamlit app wrapping the final model, with an explanation for every prediction it makes

**Stack:** Python, SQLite, pandas, scikit-learn, SHAP, Streamlit, matplotlib/seaborn

## Key findings

- **The target is imbalanced.** 79% of reports are marked serious, 21% are not. This shaped every modeling decision that followed.
- **A real data quality bug was found and fixed.** Patient age was recorded in six different units (years, decades, months, weeks, days, hours) without conversion, producing implausible values (a recorded maximum age of over 33,000). This was traced to the `patientonsetageunit` field and corrected with a proper unit conversion.
- **Drug identity matters, but not in the direction expected.** The proportion of reports marked serious ranges from 58% (Gabapentin) to 92% (Apixaban) across the 15 drugs. Oxycodone and Gabapentin, both flagged for known safety and misuse concerns in the wider literature, did not rank among the highest, which ran counter to the initial expectation going into the analysis.
- **A silent data bug nearly undercounted a third of the data.** Matching drug names by exact string comparison missed real variants like "SERTRALINE HCL" or "IBUPROFEN." with trailing punctuation, dropping 35% of relevant reports. Fixed by switching to substring matching plus a cleanup step mapping messy names to their clean target drug.

## Model performance and methodology

The modeling process is documented in full in `notebooks/modeling.ipynb`, including the parts that did not work on the first attempt.

A first logistic regression baseline collapsed to predicting "serious" for every single report, a trivial solution that still achieved 79% accuracy while learning nothing. This was diagnosed by looking past accuracy into the confusion matrix, and fixed with `class_weight="balanced"`.

The default 0.5 decision threshold was then evaluated against the project's actual priority: for a safety signal tool, missing a genuinely serious report is worse than a false alarm. A threshold of 0.35 was chosen instead, based on concrete numbers (catching 96% of real serious cases versus lower recall at higher thresholds).

The model was then improved with richer features: drug identity (one binary column per target drug, since a report can mention several drugs at once) and a proper one hot encoding for patient sex, which had originally been fed in as a raw ordered number. This improved performance at every threshold tested, and the threshold was re-tuned to 0.30 on the improved model.

**Final model:** logistic regression, `class_weight="balanced"`, 21 features (reaction count, drug count, patient age, 15 drug identity flags, 3 patient sex categories), features scaled with `StandardScaler`, decision threshold 0.30.

At this threshold, the model catches approximately 94% of reports that are actually serious, while also meaningfully distinguishing the not serious class, a real improvement over the initial baseline's inability to identify not serious reports at all.

SHAP confirms, through an independent method, what EDA and the model's own coefficients already suggested: reaction count and drug count are the most consistently influential predictors, while patient age contributes little on average, even though it can matter for individual cases.

## Limitations

- FAERS is a voluntary reporting system. A report existing does not establish that a drug caused the event, and there is no defined denominator, so nothing here should be read as a measure of a drug's real world risk [1, 2, 6, 8].
- Drug name matching is based on generic names and common variants. Brand names (for example LANTUS for Insulin glargine, ZOLOFT for Sertraline) are not matched to their generic drug and are undercounted in the drug identity features.
- The FDA's own guidance notes known reporting biases, including the Weber effect (reporting peaks around two years after approval) [3] and stimulated reporting following FDA safety alerts [4].
- This is a portfolio and demo project, not a clinical or diagnostic tool.

Full citations for every claim above are in `fda_references.md`.

## Project structure

```
src/
  fetch_data.py            fetch and paginate reports from the openFDA API
  build_database.py        build the reports/drugs/reactions database, deduplicated
  feature_engineering.py   SQL based feature engineering, including the age unit fix
  train_model.py           full training pipeline, saves model/scaler/feature order
  drugs.py                 the 15 target drugs
notebooks/
  eda.ipynb                exploratory analysis, cited findings
  modeling.ipynb           model training, evaluation, SHAP
app/
  app.py                   the Streamlit demo
models/                    saved model, scaler, and feature column order
fda_references.md          full reference list for every cited claim
```

## Running it locally

The live demo is the easiest way to try this. To run it yourself:

```
git clone https://github.com/anastasia-mistreanu/fda-adverse-event-detector.git
cd fda-adverse-event-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own free openFDA API key (get one at https://open.fda.gov/apis/authentication/).

Then, in order:

```
python3 src/build_database.py
python3 src/feature_engineering.py
python3 src/train_model.py
streamlit run app/app.py
```

## References

See `fda_references.md` for the full numbered list, including sources for every clinical and methodological claim made in this README and in `notebooks/eda.ipynb`.