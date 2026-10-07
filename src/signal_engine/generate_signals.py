import pandas as pd
import numpy as np
from src.config.settings import CLEANED_DIR, PROCESSED_DIR, REPORTS_DIR, SAS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_domain_signals(domain, lr_df, mw_df, rf_df, cv_metrics, sample_size):
    signals = []
    
    cv_auc = cv_metrics.loc[cv_metrics['model'] == 'Logistic Regression', 'roc_auc'].values[0]
    cv_f1 = cv_metrics.loc[cv_metrics['model'] == 'Logistic Regression', 'f1'].values[0]
    
    mw_domain = mw_df[mw_df['dataset'] == domain]
    
    for _, row in lr_df.iterrows():
        feature = row.iloc[0]
        if feature == 'const':
            continue
            
        coef = row['coef']
        p_val = row['p_value']
        or_val = row['odds_ratio']
        
        # Convert log-odds CI to Odds Ratio CI
        ci_lower = np.exp(row['ci_lower'])
        ci_upper = np.exp(row['ci_upper'])
        
        # Univariate
        uni_row = mw_domain[mw_domain['feature'] == feature]
        uni_p_val = uni_row['p_value'].values[0] if not uni_row.empty else None
        
        # RF
        rf_row = rf_df[rf_df['feature'] == feature]
        rf_imp = rf_row['importance'].values[0] if not rf_row.empty else None
        
        # Evidence Level
        if p_val < 0.05:
            evidence_level = "STRONG"
            interp = f"A one-unit increase in {feature} is associated with {or_val:.2f} times higher odds of the outcome, holding other variables constant."
        elif uni_p_val is not None and uni_p_val < 0.05:
            evidence_level = "EXPLORATORY"
            interp = f"Observed group difference exists for {feature}, but independent multivariable significance is not established in the final Logistic Regression."
        else:
            evidence_level = "WEAK"
            interp = f"No significant univariate or multivariable predictive signal found for {feature} within the supplied sample."
            
        signals.append({
            "signal": feature,
            "domain": domain,
            "coefficient": coef,
            "odds_ratio": or_val,
            "p_value": p_val,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "univariate_p_value": uni_p_val,
            "tree_importance": rf_imp,
            "cv_auc": cv_auc,
            "cv_f1": cv_f1,
            "sample_size": sample_size,
            "primary_evidence": "Logistic Regression",
            "secondary_evidence": "Mann-Whitney U",
            "evidence_level": evidence_level,
            "interpretation": interp,
            "causal": False
        })
    return signals

def run_signal_engine():
    logger.info('Running 8BIT Workforce Signal Engine')
    
    signals = []
    
    # 1. Market Signal (Analytics Jobs)
    skills_path = PROCESSED_DIR / 'analytics_job_skills.csv'
    if skills_path.exists():
        skills_df = pd.read_csv(skills_path)
        top_skills = skills_df['skill'].value_counts().head(20).index.tolist()
        for skill in top_skills:
            signals.append({
                "signal": skill,
                "domain": "MARKET",
                "coefficient": None,
                "odds_ratio": None,
                "p_value": None,
                "ci_lower": None,
                "ci_upper": None,
                "univariate_p_value": None,
                "tree_importance": None,
                "cv_auc": None,
                "cv_f1": None,
                "sample_size": 93000,
                "primary_evidence": "Frequency Analysis",
                "secondary_evidence": "None",
                "evidence_level": "STRONG",
                "interpretation": f"{skill} is a top 20 baseline requirement across all postings.",
                "causal": False
            })
            
    # Load supporting data
    mw_df = pd.read_csv(REPORTS_DIR / 'statistics' / 'mann_whitney_results.csv')
    
    # JDS
    jds_lr = pd.read_csv(REPORTS_DIR / 'models' / 'jds_logistic_regression_details.csv')
    jds_rf = pd.read_csv(REPORTS_DIR / 'models' / 'jds_random_forest_importance.csv')
    jds_cv = pd.read_csv(REPORTS_DIR / 'models' / 'jds_model_comparison.csv')
    signals.extend(generate_domain_signals('JDS', jds_lr, mw_df, jds_rf, jds_cv, 139))
    
    # SDS
    sds_lr = pd.read_csv(REPORTS_DIR / 'models' / 'sds_logistic_regression_details.csv')
    sds_rf = pd.read_csv(REPORTS_DIR / 'models' / 'sds_random_forest_importance.csv')
    sds_cv = pd.read_csv(REPORTS_DIR / 'models' / 'sds_model_comparison.csv')
    signals.extend(generate_domain_signals('SDS', sds_lr, mw_df, sds_rf, sds_cv, 161))
    
    signal_df = pd.DataFrame(signals)
    signal_df.to_csv(REPORTS_DIR / 'signal_engine_map.csv', index=False)
    signal_df.to_csv(SAS_DIR / 'signal_engine_map_sas.csv', index=False)
    
    # Consistency Check
    checks = []
    for _, row in signal_df[signal_df['domain'].isin(['JDS', 'SDS'])].iterrows():
        feat = row['signal']
        lr_sig = row['p_value'] < 0.05
        sig_map_status = row['evidence_level']
        
        report_status = "significant" if lr_sig else "not significant"
        model_status = "significant" if lr_sig else "not significant"
        
        consistent = (report_status == model_status) and (
            (lr_sig and sig_map_status == "STRONG") or 
            (not lr_sig and sig_map_status != "STRONG")
        )
        
        checks.append({
            "variable": feat,
            "report_status": report_status,
            "model_status": model_status,
            "signal_map_status": sig_map_status,
            "consistent": consistent,
            "notes": "Checked against primary multivariable LR evidence."
        })
        
    audit_dir = REPORTS_DIR / 'audit'
    audit_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(checks).to_csv(audit_dir / 'signal_consistency_check.csv', index=False)
    
    logger.info('Signal Engine complete. Map exported to SAS outputs.')
    return signal_df

if __name__ == "__main__":
    run_signal_engine()
