import pandas as pd
from src.config.settings import CLEANED_DIR, PROCESSED_DIR, REPORTS_DIR, SAS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_signal_engine():
    logger.info('Running 8BIT Workforce Signal Engine')
    
    signals = []
    
    # 1. Market Signal (from Analytics Jobs skills)
    skills_path = PROCESSED_DIR / 'analytics_job_skills.csv'
    if skills_path.exists():
        skills_df = pd.read_csv(skills_path)
        top_skills = skills_df['skill'].value_counts().head(20).index.tolist()
        for skill in top_skills:
            signals.append({
                'skill_or_capability': skill,
                'market_signal': 'HIGH DEMAND',
                'jds_signal': None,
                'sds_relevance': None,
                'evidence_level': 'STRONG',
                'supporting_metric': 'Top 20 skill by frequency',
                'interpretation': f'{skill} is highly requested in Analytics job postings.'
            })
            
    # 2. Capability Signal (from JDS)
    jds_stats_path = REPORTS_DIR / 'statistics' / 'mann_whitney_results.csv'
    if jds_stats_path.exists():
        jds_stats = pd.read_csv(jds_stats_path)
        jds_stats = jds_stats[jds_stats['dataset'] == 'JDS']
        for _, row in jds_stats.iterrows():
            if row['significant']:
                signals.append({
                    'skill_or_capability': row['feature'],
                    'market_signal': None,
                    'jds_signal': 'PREDICTS JUNIOR SALARY HIKE',
                    'sds_relevance': None,
                    'evidence_level': 'STRONG' if row['p_value'] < 0.01 else 'MODERATE',
                    'supporting_metric': f'Mann-Whitney p={row["p_value"]:.4f}',
                    'interpretation': f'{row["feature"]} is significantly associated with high salary hikes for junior roles.'
                })
                
    # 3. Success Signal (from SDS)
    sds_stats_path = REPORTS_DIR / 'statistics' / 'mann_whitney_results.csv'
    if sds_stats_path.exists():
        sds_stats = pd.read_csv(sds_stats_path)
        sds_stats = sds_stats[sds_stats['dataset'] == 'SDS']
        for _, row in sds_stats.iterrows():
            if row['significant']:
                signals.append({
                    'skill_or_capability': row['feature'],
                    'market_signal': None,
                    'jds_signal': None,
                    'sds_relevance': 'PREDICTS SENIOR SUCCESS',
                    'evidence_level': 'STRONG' if row['p_value'] < 0.01 else 'MODERATE',
                    'supporting_metric': f'Mann-Whitney p={row["p_value"]:.4f}',
                    'interpretation': f'{row["feature"]} is significantly associated with success in senior/customer-facing roles.'
                })
                
    signal_df = pd.DataFrame(signals)
    signal_df.to_csv(REPORTS_DIR / 'signal_engine_map.csv', index=False)
    signal_df.to_csv(SAS_DIR / 'signal_engine_map_sas.csv', index=False)
    
    logger.info('Signal Engine complete. Map exported to SAS outputs.')
    return signal_df
