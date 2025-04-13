import pandas as pd
import re

# Define the file path
csv_file_path = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Suicide Opioid Alcohol\US_Mortality_2019_2023.csv"
df = pd.read_csv(csv_file_path, low_memory=False)

# Clean up column names
df.columns = df.columns.str.strip()

# === ICD-10 code sets ===

# Suicide
suicide_ucod_codes = {f"X{str(i)}" for i in range(60, 85)}
suicide_ucod_codes.add("Y87.0")

# Opioid
opioid_ucod_codes = {'X40', 'X41', 'X42', 'X43', 'X44',
                     'X60', 'X61', 'X62', 'X63', 'X64',
                     'X85', 'Y10', 'Y11', 'Y12', 'Y13', 'Y14'}
opioid_mcod_codes = {'T40.0', 'T40.1', 'T40.2', 'T40.3', 'T40.4', 'T40.6'}

# Alcohol
alcohol_ucod_prefixes1 = {f"F10.{i}" for i in range(1, 9)}
alcohol_ucod_prefixes2 = {f"F70.{i}" for i in range(0, 4)}
alcohol_ucod_codes = {'G31.2', 'G62.1', 'G72.1', 'I42.6', 'K29.2', 'K70.9',
                      'K85.2', 'K86.0', 'Q86.0', 'P04.3', 'X45', 'Y15', 'X65'}
alcohol_ucod_codes.update(alcohol_ucod_prefixes1)
alcohol_ucod_codes.update(alcohol_ucod_prefixes2)

# === Helper functions ===

def check_suicide(ucod):
    return str(ucod).strip() in suicide_ucod_codes

def check_opioid(ucod, mcod):
    # Clean and split MCODs on both ";" and space
    if pd.isnull(mcod):
        mcod_list = []
    else:
        mcod_list = re.split(r'[; ]+', str(mcod))
        mcod_list = [code.strip() for code in mcod_list if code.strip()]
    
    return (str(ucod).strip() in opioid_ucod_codes) or any(code in opioid_mcod_codes for code in mcod_list)

def check_alcohol(ucod):
    ucod = str(ucod).strip()
    return ucod in alcohol_ucod_codes or any(ucod.startswith(prefix.split('.')[0]) for prefix in alcohol_ucod_prefixes1)

# === Apply classification ===
df['is_suicide'] = df['icd_10'].apply(check_suicide)
df['is_opioid'] = df.apply(lambda row: check_opioid(row['icd_10'], row['MCODs']), axis=1)
df['is_alcohol'] = df['icd_10'].apply(check_alcohol)

def classify_combination(row):
    tags = []
    if row['is_suicide']:
        tags.append("Suicide")
    if row['is_opioid']:
        tags.append("Opioid")
    if row['is_alcohol']:
        tags.append("Alcohol")
    return " + ".join(tags) if tags else "Other"

df['cause_combination'] = df.apply(classify_combination, axis=1)

# === Save results ===

# Save all tagged rows
tagged_path = csv_file_path.replace(".csv", "_tagged.csv")
df.to_csv(tagged_path, index=False)

# Save only deaths of despair
deaths_of_despair = df[df['cause_combination'] != "Other"]
filtered_path = csv_file_path.replace(".csv", "_deaths_of_despair_only.csv")
deaths_of_despair.to_csv(filtered_path, index=False)

print(f"✅ Tagged data saved to: {tagged_path}")
print(f"✅ Filtered 'deaths of despair' saved to: {filtered_path}")
