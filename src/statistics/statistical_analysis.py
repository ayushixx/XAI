import pandas as pd
from scipy.stats import mannwhitneyu
from src.config.settings import CLEANED_DIR, REPORTS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_statistics():
    logger.info('Running Statistical Analysis')
    results = []
    
    # JDS
    jds_path = CLEANED_DIR / 'cleaned_jds.csv'
    if jds_path.exists():
        jds = pd.read_csv(jds_path)
        skills = ['big_data_skills', 'maths-stats_skills', 'coding_skills', 'ai_and_ml_skills', 'dashboard_and_storytelling_skills']
        for s in skills:
            if s in jds.columns:
                high = jds[jds['target'] == 1][s].dropna()
                low = jds[jds['target'] == 0][s].dropna()
                if len(high) > 0 and len(low) > 0:
                    stat, p = mannwhitneyu(high, low)
                    results.append({'dataset': 'JDS', 'feature': s, 'p_value': p, 'significant': p < 0.05})
                    
    # SDS
    sds_path = CLEANED_DIR / 'cleaned_sds.csv'
    if sds_path.exists():
        sds = pd.read_csv(sds_path)
        traits = ['neuroticism', 'extraversion', 'openness_to_experience', 'agreeableness', 'conscientiousness']
        for t in traits:
            if t in sds.columns:
                high = sds[sds['target'] == 1][t].dropna()
                low = sds[sds['target'] == 0][t].dropna()
                if len(high) > 0 and len(low) > 0:
                    stat, p = mannwhitneyu(high, low)
                    results.append({'dataset': 'SDS', 'feature': t, 'p_value': p, 'significant': p < 0.05})
                    
    res_df = pd.DataFrame(results)
    res_df.to_csv(REPORTS_DIR / 'statistics' / 'mann_whitney_results.csv', index=False)
    logger.info('Statistical Analysis Complete.')
    return res_df
