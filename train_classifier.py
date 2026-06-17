import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

# -----------------------------
# LOAD BOTH FEATURE SETS
# -----------------------------
print("Loading features...")

# Hand-crafted features (Step 1)
hc_df  = pd.read_csv("features.csv")
hc_cols = [c for c in hc_df.columns if c.startswith("feat_")]

# Wav2Vec2 features (Step 3)
w2v_df  = pd.read_csv("wav2vec2_features.csv")
w2v_cols = [c for c in w2v_df.columns if c.startswith("w2v_")]

# Merge on filename so rows align correctly
merged = pd.merge(
    hc_df[["filename","label","label_name"] + hc_cols],
    w2v_df[["filename"] + w2v_cols],
    on="filename"
)

print(f"Hand-crafted features : {len(hc_cols)}")
print(f"Wav2Vec2 features     : {len(w2v_cols)}")
print(f"Combined features     : {len(hc_cols)+len(w2v_cols)}")
print(f"Total samples         : {len(merged)}")
print(f"Label distribution    :\n{merged['label_name'].value_counts()}\n")

all_feat_cols = hc_cols + w2v_cols
X = merged[all_feat_cols].values
y = merged["label"].values

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

print(f"Train: {len(X_train)} | Test: {len(X_test)}\n")

# -----------------------------
# TRAIN XGBOOST
# -----------------------------
print("Training XGBoost on combined features...")
xgb = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=sum(y==0)/sum(y==1),
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)
xgb.fit(X_train, y_train)
pred = xgb.predict(X_test)
acc  = accuracy_score(y_test, pred)

print(f"\nCombined Features Accuracy: {acc*100:.2f}%")
print("\n--- Classification Report ---")
print(classification_report(
    y_test, pred,
    target_names=["Non-Dysarthric", "Dysarthric"]
))

cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Non-Dysarthric","Dysarthric"],
            yticklabels=["Non-Dysarthric","Dysarthric"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Combined Features — Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix_combined.png", dpi=150)
plt.show()
print("Saved confusion_matrix_combined.png")

# -----------------------------
# SAVE FINAL MODEL + SCALER
# -----------------------------
joblib.dump(xgb,    "dysarthria_model_final.pkl")
joblib.dump(scaler, "scaler_final.pkl")

print(f"\nSaved: dysarthria_model_final.pkl")
print(f"Saved: scaler_final.pkl")
print(f"\nStep 3 complete. Ready for Step 4 (Phoneme error detection).")
