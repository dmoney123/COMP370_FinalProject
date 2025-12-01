import pandas as pd

df = pd.read_csv("/Users/cindy/PycharmProjects/COMP370/pos_neg_neutral/370 final project - Annotated Topics.csv")

# Clean and standardize labels
col = "Positive/Negative/Neutral"
df[col] = df[col].astype(str).str.strip()  # remove spaces
df[col] = df[col].replace({"": "N/A", "nan": "N/A"})  # handle empty or nan strings

# Count values + percentages
counts = df[col].value_counts(dropna=False)
percentages = (counts / len(df)) * 100

result = pd.DataFrame({"Count": counts, "Percent": percentages.round(2)})
print(result)