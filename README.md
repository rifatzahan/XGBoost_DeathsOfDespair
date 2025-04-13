# 🧠 XGBoost-Based Analysis of Deaths of Despair (Suicide, Opioid, Alcohol)

This project analyzes U.S. mortality data (2019–2023) to identify and visualize deaths due to **suicide**, **opioid overdose**, and **alcohol-related causes**, collectively known as _deaths of despair_. It leverages **ICD-10 codes**, **XGBoost modeling**, and **SHAP explainability** to identify risk patterns based on socio-demographic variables.

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `1 merge_us_deaths_files.py` | Merges raw CDC mortality flat files (2019–2023) into a single CSV. Extracts key UCOD & MCOD variables. |
| `2 deaths_of_Despair_Extraction.py` | Tags each death as Suicide, Opioid, Alcohol, or their combinations based on ICD-10 codes. |
| `3 variable_recode.py` | Recodes demographic variables: sex, age, race, marital status, education, and occupation for analysis. |
| `4 normalized_heatmap.py` | Generates interactive heatmaps, stacked bar plots, and trend plots using Plotly. Saves results to HTML. |
| `xgboost_shap_pipeline.py` | Trains an XGBoost classifier to predict cause of death. Visualizes SHAP values for interpretability. |

---

## 🔬 Research Goals

1. **Identify deaths of despair** using structured cause-of-death codes.
2. **Explore patterns** in deaths by demographic groups using visualizations.
3. **Build a predictive model** for cause of death (suicide, opioid, alcohol).
4. **Explain model decisions** using SHAP to uncover high-risk profiles.

---

## 📊 Key Features

- ✅ ICD-10 classification for suicide, opioid, and alcohol deaths
- ✅ Data cleaning and harmonization across 5 years
- ✅ Recode for public health–friendly variables
- ✅ SHAP plots to visualize nonlinear risk patterns
- ✅ Plotly-based interactive dashboards

---

## 📦 Dependencies

```bash
pip install pandas numpy xgboost shap matplotlib seaborn plotly scikit-learn
