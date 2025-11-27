import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to your Excel file (relative to script directory)
excel_path = os.path.join(script_dir, "Annotated_Topics.xlsx")

# Read Excel file into DataFrame
df = pd.read_excel(excel_path)

# Display basic info about the dataframe before cleaning
print(f"Original shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

# Remove rows where topic label column contains N/A
# Handle different N/A representations (NaN, "N/A", "NA", empty strings, etc.)
topic_column = "Topic Label"  # Column name with capital letters

# Create a mask to filter out N/A values in various forms
mask = (
    df[topic_column].notna() &  # Not NaN/null
    (df[topic_column].astype(str).str.upper().str.strip() != "N/A") &  # Not "N/A" (case-insensitive)
    (df[topic_column].astype(str).str.upper().str.strip() != "NA") &   # Not "NA" (case-insensitive)
    (df[topic_column].astype(str).str.strip() != "") &  # Not empty string
    (df[topic_column].astype(str).str.strip() != "nan")  # Not string "nan"
)

df_clean = df[mask]

# Display info after cleaning
print(f"\nCleaned shape: {df_clean.shape}")
print(f"Removed {len(df) - len(df_clean)} rows")

# Save cleaned data to CSV
output_path = os.path.join(script_dir, "clean.csv")
df_clean.to_csv(output_path, index=False)
print(f"\nSaved cleaned dataframe to: {output_path}")
print(f"\nFirst few rows of cleaned data:")
print(df_clean.head())

# Compute topic frequencies across all from_json values
print(f"\nUnique from_json values: {df_clean['from_json'].unique()}")
print(f"\nUnique topics: {df_clean[topic_column].unique()}")

# Create a crosstab: rows = from_json, columns = topics, values = frequencies
topic_freq = pd.crosstab(df_clean['from_json'], df_clean[topic_column])

# Reset index to make from_json a column instead of index
topic_freq = topic_freq.reset_index()

# Display the frequency table
print(f"\nTopic frequency table shape: {topic_freq.shape}")
print(f"\nTopic frequency table:")
print(topic_freq)

# Save topic frequencies to CSV
freq_output_path = os.path.join(script_dir, "topic_frequencies.csv")
topic_freq.to_csv(freq_output_path, index=False)
print(f"\nSaved topic frequencies to: {freq_output_path}")

# Compute percentage frequencies (percentages within each from_json value)
# First, recreate the crosstab without reset_index to calculate percentages
topic_freq_pct = pd.crosstab(df_clean['from_json'], df_clean[topic_column])

# Calculate percentages: divide each value by row sum and multiply by 100
topic_freq_pct = topic_freq_pct.div(topic_freq_pct.sum(axis=1), axis=0) * 100

# Round to 2 decimal places for readability
topic_freq_pct = topic_freq_pct.round(2)

# Reset index to make from_json a column instead of index
topic_freq_pct = topic_freq_pct.reset_index()

# Display the percentage frequency table
print(f"\nTopic percentage frequency table shape: {topic_freq_pct.shape}")
print(f"\nTopic percentage frequency table:")
print(topic_freq_pct)

# Save percentage frequencies to CSV
pct_output_path = os.path.join(script_dir, "percent_topic_frequency.csv")
topic_freq_pct.to_csv(pct_output_path, index=False)
print(f"\nSaved percentage topic frequencies to: {pct_output_path}")

# Create bar graph from percentage topic frequency
# Set from_json as index for easier plotting
topic_freq_pct_plot = topic_freq_pct.set_index('from_json')

# Create the figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Get the number of topics and from_json values
n_topics = len(topic_freq_pct_plot.columns)
n_groups = len(topic_freq_pct_plot.index)

# Set up the bar positions
x = np.arange(n_topics)
width = 0.12  # Width of bars (adjusted for 6 groups)

# Create bars for each from_json value
colors = plt.cm.Set3(np.linspace(0, 1, n_groups))
for i, (idx, row) in enumerate(topic_freq_pct_plot.iterrows()):
    offset = (i - n_groups/2 + 0.5) * width
    ax.bar(x + offset, row.values, width, label=idx, color=colors[i], alpha=0.8)

# Customize the plot
ax.set_xlabel('Topics', fontsize=12, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax.set_title('Topic Frequency Percentages by Source', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(topic_freq_pct_plot.columns, rotation=45, ha='right')
ax.legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the figure
graph_output_path = os.path.join(script_dir, "percent_topic_frequency_bar.png")
plt.savefig(graph_output_path, dpi=300, bbox_inches='tight')
print(f"\nSaved bar graph to: {graph_output_path}")

# Display the plot
plt.show()



