import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("/Users/cindy/PycharmProjects/COMP370/pos_neg_neutral/370 final project - Annotated Topics.csv")

sent_col = "Positive/Negative/Neutral"

# --- Clean sentiment labels ---
df[sent_col] = df[sent_col].astype(str).str.strip()
df[sent_col] = df[sent_col].replace({"": "N/A", "nan": "N/A"})

# --- Define pre vs post election ---
df["Period"] = "Other"
df.loc[df["from_json"].str.contains("pre", case=False, na=False), "Period"] = "Pre-election"
df.loc[df["from_json"].str.contains("post", case=False, na=False), "Period"] = "Post-election"

# Keep only relevant rows
df = df[df["Period"].isin(["Pre-election", "Post-election"])]

# --- Count and percentage ---
counts = df.groupby(["Period", sent_col]).size().unstack(fill_value=0)

# Remove N/A
if "N/A" in counts.columns:
    counts = counts.drop(columns=["N/A"])

# Percentages
percentages = counts.div(counts.sum(axis=1), axis=0) * 100
percentages = percentages.loc[["Pre-election", "Post-election"]]

# --- MATCH COLORS TO BOTTOM FIGURE ---
blue = "#0000FF"     # Left color (Pre)
red = "#FF0000"      # Right color (Post)

# --- Plot setup ---
sentiments = list(percentages.columns)
x = np.arange(len(sentiments))
width = 0.22

pre_vals = percentages.loc["Pre-election"]
post_vals = percentages.loc["Post-election"]

fig, ax = plt.subplots(figsize=(9, 5))

# Bars
bars_pre = ax.bar(x - width/2, pre_vals, width, label="Pre-election", alpha=1.0, color=blue)
bars_post = ax.bar(x + width/2, post_vals, width, label="Post-election", alpha=1.0, color=red)

# Labels
ax.set_title("Sentiment Distribution (Pre vs Post Election)")
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Sentiment Category")
ax.set_xticks(x)
ax.set_xticklabels(sentiments)
ax.legend()

# --- Add % labels ---
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', fontsize=9)

add_labels(bars_pre)
add_labels(bars_post)

# --- Add slanted connecting lines + change annotation ---
for i, cat in enumerate(sentiments):
    pre = pre_vals[i]
    post = post_vals[i]

    x_pre = x[i] - width/2
    x_post = x[i] + width/2
    mid_x = (x_pre + x_post) / 2

    change = post - pre
    line_color = "green" if change >= 0 else "red"

    # line between pre and post
    ax.plot([x_pre, x_post], [pre, post], color=line_color, linewidth=1.8)

    # % change label (slightly above)
    y_text = max(pre, post) + 1.0
    ax.text(mid_x, y_text, f"{change:+.1f}%", ha="center", fontsize=9,
            color=line_color, fontweight="bold")

plt.tight_layout()
plt.show()
