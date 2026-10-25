"""
Copy your hand labels from cold_20.csv into the first 20 rows of labels.csv.

cold_20.csv holds only the 20 cold posts, so you can label them without the
pre-labelled rows in view. Fill its `label` column with analysis / take /
reaction, save, then run:

    .venv/bin/python scripts/merge_cold.py
"""

import sys

import pandas as pd

LABELS = {"analysis", "take", "reaction"}

cold = pd.read_csv("cold_20.csv", keep_default_na=False)
df = pd.read_csv("labels.csv", keep_default_na=False)

cold["label"] = cold["label"].str.strip()
bad = cold[~cold["label"].isin(LABELS)]
if len(bad):
    sys.exit(f"Rows {bad['row'].tolist()} in cold_20.csv need one of {sorted(LABELS)}.")

for row, text, label in zip(cold["row"], cold["text"], cold["label"]):
    if df.at[row, "text"] != text:
        sys.exit(f"Row {row} text doesn't match labels.csv — was labels.csv reordered?")
    df.at[row, "label"] = label
    df.at[row, "note"] = "cold"

df.to_csv("labels.csv", index=False)
print("Merged 20 cold labels into labels.csv.")
print(df["label"].value_counts().to_string())
