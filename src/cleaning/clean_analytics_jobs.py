import pandas as pd
import re
from src.config.settings import RAW_DIR, CLEANED_DIR, PROCESSED_DIR, AUDIT_DIR, FILE_MAPPING
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_analytics_jobs():
    logger.info('Cleaning Analytics Jobs dataset')
    filepath = RAW_DIR / FILE_MAPPING['analytics_jobs']
    if not filepath.exists():
        return None
    df = pd.read_csv(filepath)
    initial_rows = len(df)
    
    df.columns = df.columns.str.strip().str.lower()
    
    missing_job_types = df['job_type'].isnull().sum()
    df['job_type'] = df['job_type'].fillna('Analytics')
    
    skills_list = []
    for idx, row in df.iterrows():
        skills = str(row.get('key_skills', ''))
        if skills != 'nan' and skills != '':
            split_skills = re.split(r'[,|;]', skills)
            for s in split_skills:
                s_clean = s.strip().lower()
                if s_clean:
                    skills_list.append({
                        'job_id': row.get('s_no', idx),
                        'job_designation': row.get('job_desig', ''),
                        'skill': s_clean
                    })
    
    skills_df = pd.DataFrame(skills_list).drop_duplicates()
    skills_df.to_csv(PROCESSED_DIR / 'analytics_job_skills.csv', index=False)
    
    cleaning_log = pd.DataFrame([{
        'dataset': 'analytics_jobs',
        'column': 'job_type',
        'issue': 'missing values',
        'action': 'filled with Analytics',
        'rows_affected': missing_job_types,
        'reason': 'domain assumption'
    }])
    cleaning_log.to_csv(AUDIT_DIR / 'cleaning_log_analytics_jobs.csv', index=False)
    
    df.to_csv(CLEANED_DIR / 'cleaned_analytics_jobs.csv', index=False)
    logger.info(f'Cleaned Analytics Jobs: extracted {len(skills_df)} skill entries.')
    return df
