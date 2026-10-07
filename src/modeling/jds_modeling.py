import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib
from src.config.settings import CLEANED_DIR, MODELS_DIR, REPORTS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def train_jds():
    logger.info('Training JDS Models')
    filepath = CLEANED_DIR / 'cleaned_jds.csv'
    if not filepath.exists():
        return None
        
    df = pd.read_csv(filepath)
    features = ['big_data_skills', 'maths-stats_skills', 'coding_skills', 'ai_and_ml_skills', 'dashboard_and_storytelling_skills']
    features = [f for f in features if f in df.columns]
    
    df = df.dropna(subset=features + ['target'])
    X = df[features]
    y = df['target']
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
        'Random Forest': RandomForestClassifier(random_state=42)
    }
    
    results = []
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    best_model = None
    best_auc = 0
    best_name = ''
    
    for name, clf in models.items():
        scores = cross_validate(clf, X, y, cv=cv, scoring=['accuracy', 'roc_auc', 'f1'])
        auc = scores['test_roc_auc'].mean()
        f1 = scores['test_f1'].mean()
        acc = scores['test_accuracy'].mean()
        
        results.append({'model': name, 'accuracy': acc, 'roc_auc': auc, 'f1': f1})
        
        clf.fit(X, y)
        joblib.dump(clf, MODELS_DIR / 'jds' / f'{name.replace(" ", "_").lower()}.pkl')
        
        # Feature importances for trees
        if hasattr(clf, 'feature_importances_'):
            imp_df = pd.DataFrame({'feature': features, 'importance': clf.feature_importances_})
            imp_df.to_csv(REPORTS_DIR / 'models' / f'jds_{name.replace(" ", "_").lower()}_importance.csv', index=False)
        
        # Determine best model based on validation performance and interpretability preference
        if auc > best_auc:
            best_auc = auc
            best_model = clf
            best_name = name
            
    # Prefer Logistic Regression if it's very close (e.g. within 0.02 AUC) due to interpretability
    for r in results:
        if r['model'] == 'Logistic Regression' and (best_auc - r['roc_auc']) < 0.02:
            best_name = 'Logistic Regression'
            best_model = models['Logistic Regression']
            best_auc = r['roc_auc']

    res_df = pd.DataFrame(results)
    res_df.to_csv(REPORTS_DIR / 'models' / 'jds_model_comparison.csv', index=False)
    
    logger.info(f'JDS Training Complete. Best model selected: {best_name} with AUC {best_auc:.3f}')
    
    # Generate detailed stats for Logistic Regression using statsmodels
    logger.info('Generating detailed statistical interpretation for JDS')
    X_sm = sm.add_constant(X)
    logit_model = sm.Logit(y, X_sm)
    try:
        result = logit_model.fit(disp=0)
        
        summary_df = pd.DataFrame({
            'coef': result.params,
            'std_err': result.bse,
            'z': result.tvalues,
            'p_value': result.pvalues,
            'ci_lower': result.conf_int()[0],
            'ci_upper': result.conf_int()[1],
            'odds_ratio': np.exp(result.params)
        })
        summary_df['significant'] = summary_df['p_value'] < 0.05
        summary_df.to_csv(REPORTS_DIR / 'models' / 'jds_logistic_regression_details.csv', index=True)
    except Exception as e:
        logger.error(f'Could not fit statsmodels Logit for JDS: {e}')
        
    return res_df, best_model, features
