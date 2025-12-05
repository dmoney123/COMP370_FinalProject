import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv("/Users/cindy/PycharmProjects/COMP370/pos_neg_neutral/370 final project - Annotated Topics.csv")

sent_col = "Positive/Negative/Neutral"

# --- Clean sentiment labels ---
df[sent_col] = df[sent_col].astype(str).str.strip()
df[sent_col] = df[sent_col].replace({"": "N/A", "nan": "N/A"})

# --- Determine political orientation ---
def extract_orientation(filename):
    filename = filename.lower()
    if "left" in filename:
        return "Left"
    elif "right" in filename:
        return "Right"
    elif "center" in filename or "centre" in filename:
        return "Center"
    else:
        return "Other"

df["Orientation"] = df["from_json"].apply(extract_orientation)

# Keep only Left / Right / Center
df = df[df["Orientation"].isin(["Left", "Right", "Center"])]

# --- Count sentiment per orientation ---
counts = df.groupby(["Orientation", sent_col]).size().unstack(fill_value=0)

# 🔥 REMOVE N/A completely
if "N/A" in counts.columns:
    counts = counts.drop(columns=["N/A"])

# --- Percentages (within each orientation) ---
percentages = counts.div(counts.sum(axis=1), axis=0) * 100

# --- Plot formatting ---
orientation_order = ["Center", "Left", "Right"]
sentiment_order = ["Positive", "Negative", "Neutral"]   # N/A removed

plot_data = percentages.loc[orientation_order, sentiment_order]

x = np.arange(len(sentiment_order))
width = 0.15

fig, ax = plt.subplots(figsize=(10, 5))

# Bars
bars_center = ax.bar(x - width, plot_data.loc["Center"], width, label="Center", color="black")
bars_left   = ax.bar(x,         plot_data.loc["Left"],   width, label="Left",   color="blue")
bars_right  = ax.bar(x + width, plot_data.loc["Right"],  width, label="Right",  color="red")

# --- Add % labels above each bar ---
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', fontsize=8)

add_labels(bars_center)
add_labels(bars_left)
add_labels(bars_right)

# --- Graph settings ---
ax.set_xticks(x)
ax.set_xticklabels(sentiment_order)
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Sentiment Category")
ax.set_title("Sentiment Distribution Comparison: Left vs Right vs Center")
ax.legend()

plt.tight_layout()
plt.show()
