import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Advanced Gradient Boosting Algorithms
import xgboost as xgb
import lightgbm as lgb
import catboost as cb

from src.config.settings import CLEANED_DIR, ADVANCED_MODELS_DIR, REPORTS_DIR
from src.evaluation.metrics_engine import EnhancedMetricsEngine
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_model_zoo() -> Dict[str, Any]:
    """Instantiates the complete model zoo: Classical + Advanced Gradient Boosters."""
    return {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
        "XGBoost": xgb.XGBClassifier(
            random_state=42,
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            eval_metric="logloss"
        ),
        "LightGBM": lgb.LGBMClassifier(
            random_state=42,
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            verbose=-1
        ),
        "CatBoost": cb.CatBoostClassifier(
            random_seed=42,
            iterations=150,
            depth=4,
            learning_rate=0.08,
            verbose=0
        )
    }

def train_and_benchmark_dataset(
    dataset_name: str,
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str = 'target'
) -> Tuple[pd.DataFrame, Dict[str, Any], pd.DataFrame]:
    """
    Trains and benchmarks all 6 models with Stratified K-Fold CV,
    computing all enhanced evaluation metrics and feature importances.
    """
    logger.info(f"Training and Benchmarking Advanced Models on {dataset_name} ({len(df)} rows)")
    
    clean_df = df.dropna(subset=feature_cols + [target_col])
    X = clean_df[feature_cols]
    y = clean_df[target_col]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    zoo = get_model_zoo()
    
    metrics_records = []
    feature_importances_records = []
    trained_artifacts = {}

    target_models_dir = ADVANCED_MODELS_DIR / dataset_name.lower()
    target_models_dir.mkdir(parents=True, exist_ok=True)

    for name, clf in zoo.items():
        # Out-of-fold cross-validated predictions for robust evaluation
        y_pred = cross_val_predict(clf, X, y, cv=cv, method='predict')
        
        y_prob = None
        if hasattr(clf, 'predict_proba'):
            try:
                y_prob = cross_val_predict(clf, X, y, cv=cv, method='predict_proba')
            except Exception:
                y_prob = None

        metrics = EnhancedMetricsEngine.evaluate_binary_classifier(y, y_pred, y_prob, model_name=name)
        metrics["dataset"] = dataset_name
        metrics_records.append(metrics)

        # Fit on full dataset for inference serialization
        clf.fit(X, y)
        model_path = target_models_dir / f"{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(clf, model_path)
        trained_artifacts[name] = clf

        # Extract Feature Importance / Coefficients
        if hasattr(clf, 'feature_importances_'):
            for feat, imp in zip(feature_cols, clf.feature_importances_):
                feature_importances_records.append({
                    "dataset": dataset_name,
                    "model": name,
                    "feature": feat,
                    "importance": round(float(imp), 4)
                })
        elif hasattr(clf, 'coef_'):
            for feat, coef in zip(feature_cols, clf.coef_[0]):
                feature_importances_records.append({
                    "dataset": dataset_name,
                    "model": name,
                    "feature": feat,
                    "importance": round(float(abs(coef)), 4)
                })

    # Summary dataframe
    summary_data = []
    for m in metrics_records:
        summary_data.append({
            "dataset": m["dataset"],
            "model": m["model_name"],
            "accuracy": m["accuracy"],
            "roc_auc": m["roc_auc"],
            "f1_score": m["f1_score"],
            "precision": m["precision"],
            "recall": m["recall"],
            "balanced_accuracy": m["balanced_accuracy"],
            "brier_calibration": m["brier_calibration_score"]
        })

    comparison_df = pd.DataFrame(summary_data)
    # Sort by ROC-AUC and F1 for performance ranking
    comparison_df = comparison_df.sort_values(by=["roc_auc", "f1_score"], ascending=False).reset_index(drop=True)
    comparison_df["rank"] = comparison_df.index + 1

    fi_df = pd.DataFrame(feature_importances_records)

    # Save to reports
    out_dir = REPORTS_DIR / 'models'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    comparison_df.to_csv(out_dir / f'{dataset_name.lower()}_advanced_model_comparison.csv', index=False)
    fi_df.to_csv(out_dir / f'{dataset_name.lower()}_advanced_feature_importance.csv', index=False)
    
    with open(out_dir / f'{dataset_name.lower()}_detailed_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics_records, f, indent=2)

    # Markdown report
    md_content = EnhancedMetricsEngine.generate_markdown_report(
        metrics_records,
        title=f"Advanced Model Comparison & Rankings ({dataset_name})"
    )
    with open(out_dir / f'{dataset_name.lower()}_model_comparison.md', 'w', encoding='utf-8') as f:
        f.write(md_content)

    logger.info(f"Completed Advanced Benchmarking for {dataset_name}. Best Model: {comparison_df.iloc[0]['model']} (AUC: {comparison_df.iloc[0]['roc_auc']:.4f})")
    return comparison_df, trained_artifacts, fi_df

def run_advanced_modeling() -> Dict[str, Any]:
    """Executes advanced model training across all datasets in project."""
    logger.info("Executing Advanced Modeling Pipeline (XGBoost, LightGBM, CatBoost, RF, DT, LR)")
    
    results = {}
    
    # 1. JDS Dataset
    jds_path = CLEANED_DIR / 'cleaned_jds.csv'
    if jds_path.exists():
        jds_df = pd.read_csv(jds_path)
        jds_features = ['big_data_skills', 'maths-stats_skills', 'coding_skills', 'ai_and_ml_skills', 'dashboard_and_storytelling_skills']
        jds_features = [f for f in jds_features if f in jds_df.columns]
        jds_comp, _, _ = train_and_benchmark_dataset('JDS', jds_df, jds_features, target_col='target')
        results['jds'] = jds_comp.to_dict(orient='records')

    # 2. SDS Dataset
    sds_path = CLEANED_DIR / 'cleaned_sds.csv'
    if sds_path.exists():
        sds_df = pd.read_csv(sds_path)
        sds_features = ['extraversion', 'agreeableness', 'openness', 'conscientiousness', 'emotional_stability']
        sds_features = [f for f in sds_features if f in sds_df.columns]
        sds_comp, _, _ = train_and_benchmark_dataset('SDS', sds_df, sds_features, target_col='target')
        results['sds'] = sds_comp.to_dict(orient='records')

    logger.info("Advanced Modeling Pipeline finished successfully.")
    return results
