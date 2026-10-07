import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    balanced_accuracy_score,
    confusion_matrix,
    brier_score_loss,
    classification_report
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

class EnhancedMetricsEngine:
    """
    Standardized Comprehensive Evaluation Metrics Engine.
    Computes Accuracy, ROC-AUC, F1, Precision, Recall, Balanced Accuracy,
    Confusion Matrix, Brier Calibration Loss, and formatted reports.
    """
    @staticmethod
    def evaluate_binary_classifier(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
        model_name: str = "Classifier"
    ) -> Dict[str, Any]:
        """Calculates full evaluation suite for binary classification."""
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)

        acc = float(accuracy_score(y_true, y_pred))
        prec = float(precision_score(y_true, y_pred, zero_division=0))
        rec = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))
        bal_acc = float(balanced_accuracy_score(y_true, y_pred))
        
        # ROC-AUC & Brier Calibration
        if y_prob is not None:
            try:
                # If y_prob is 2D, take positive class
                if len(y_prob.shape) > 1 and y_prob.shape[1] > 1:
                    prob_pos = y_prob[:, 1]
                else:
                    prob_pos = y_prob
                auc = float(roc_auc_score(y_true, prob_pos))
                brier = float(brier_score_loss(y_true, prob_pos))
            except Exception:
                auc = float(roc_auc_score(y_true, y_pred))
                brier = 0.0
        else:
            try:
                auc = float(roc_auc_score(y_true, y_pred))
            except Exception:
                auc = 0.5
            brier = 0.0

        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
        
        clf_rep = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

        metrics_dict = {
            "model_name": model_name,
            "accuracy": round(acc, 4),
            "roc_auc": round(auc, 4),
            "f1_score": round(f1, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "balanced_accuracy": round(bal_acc, 4),
            "brier_calibration_score": round(brier, 4),
            "confusion_matrix": {
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp),
                "matrix_2x2": [[int(tn), int(fp)], [int(fn), int(tp)]]
            },
            "classification_report": clf_rep
        }
        return metrics_dict

    @staticmethod
    def generate_markdown_report(metrics_list: List[Dict[str, Any]], title: str = "Model Comparison Report") -> str:
        """Formats a comparison table in GitHub Markdown."""
        md = [f"# {title}\n"]
        md.append("| Model | Accuracy | ROC-AUC | F1 Score | Precision | Recall | Balanced Acc | Calibration (Brier) |")
        md.append("|---|---|---|---|---|---|---|---|")
        for m in metrics_list:
            md.append(
                f"| **{m['model_name']}** | {m['accuracy']:.4f} | {m['roc_auc']:.4f} | {m['f1_score']:.4f} | "
                f"{m['precision']:.4f} | {m['recall']:.4f} | {m['balanced_accuracy']:.4f} | {m['brier_calibration_score']:.4f} |"
            )
        return "\n".join(md)
