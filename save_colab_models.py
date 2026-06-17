#!/usr/bin/env python3
"""
Script to save trained models from Colab notebook to local Speech_Therapy folder
Run this AFTER training completes in Colab Cell 26
"""

import joblib
import pickle
import os
from datetime import datetime

OUTPUT_DIR = "/content"  # Colab root directory

def save_models_and_results():
    """Save trained models and artifacts from Colab training"""

    # Models to save (from Cell 26)
    models_dict = {
        "RandomForest": results["Random Forest"]["model"],
        "XGBoost": results["XGBoost"]["model"],
        "MLPNeuralNetwork": results["MLP Neural Network"]["model"]
    }

    # Save each model
    for model_name, model_obj in models_dict.items():
        filepath = f"{OUTPUT_DIR}/{model_name}_dysarthria.pkl"
        joblib.dump(model_obj, filepath)
        print(f"✅ Saved: {model_name} → {filepath}")

    # Save the feature selector
    selector_path = f"{OUTPUT_DIR}/feature_selector.pkl"
    joblib.dump(selector, selector_path)
    print(f"✅ Saved: Feature Selector → {selector_path}")

    # Save scaler if used
    scaler_path = f"{OUTPUT_DIR}/scaler.pkl"
    joblib.dump(scaler, scaler_path)
    print(f"✅ Saved: StandardScaler → {scaler_path}")

    # Save metadata
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "total_samples": len(X),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "n_features": X_selected.shape[1],
        "accuracy_rf": results["Random Forest"]["accuracy"],
        "accuracy_xgb": results["XGBoost"]["accuracy"],
        "accuracy_mlp": results["MLP Neural Network"]["accuracy"],
        "class_distribution": {
            "dysarthric": int(sum(y==1)),
            "non_dysarthric": int(sum(y==0))
        },
        "augmentation_method": "AddGaussianNoise + TimeStretch + PitchShift",
        "feature_extraction": "MFCC + Deltas (40 each) + RMS + ZCR + Spectral"
    }

    metadata_path = f"{OUTPUT_DIR}/model_metadata.pkl"
    joblib.dump(metadata, metadata_path)
    print(f"✅ Saved: Metadata → {metadata_path}")

    print("\n🎉 All models saved successfully!")
    print("📥 Download these files to your Speech_Therapy folder:")
    print("   - RandomForest_dysarthria.pkl")
    print("   - XGBoost_dysarthria.pkl")
    print("   - MLPNeuralNetwork_dysarthria.pkl")
    print("   - feature_selector.pkl")
    print("   - scaler.pkl")
    print("   - model_metadata.pkl")
    print("   - wav2vec2_features.csv")
    print("   - intelligibility_scores.csv")
    print("   - phoneme_error_analysis.png")

if __name__ == "__main__":
    save_models_and_results()
