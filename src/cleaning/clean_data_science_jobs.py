import pandas as pd
from src.config.settings import RAW_DIR, CLEANED_DIR, AUDIT_DIR, FILE_MAPPING
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_ds_jobs():
    logger.info('Cleaning Data Science Jobs dataset')
    filepath = RAW_DIR / FILE_MAPPING['ds_jobs']
    if not filepath.exists():
        return None
    df = pd.read_csv(filepath)
    initial_rows = len(df)
    
    # Standardize columns
    df.columns = df.columns.str.strip().str.lower()
    df['company_name'] = df['company_name'].str.strip()
    df['job_title'] = df['job_title'].str.strip()
    
    # Handle duplicates
    df = df.drop_duplicates()
    
    cleaning_log = pd.DataFrame([{
        'dataset': 'ds_jobs',
        'column': 'all',
        'issue': 'whitespace and duplicates',
        'action': 'trimmed and deduplicated',
        'rows_affected': initial_rows - len(df),
        'reason': 'standardize text and remove exact dupes'
    }])
    cleaning_log.to_csv(AUDIT_DIR / 'cleaning_log_ds_jobs.csv', index=False)
    
    df.to_csv(CLEANED_DIR / 'cleaned_ds_jobs.csv', index=False)
    logger.info(f'Cleaned DS Jobs: {len(df)} rows remain.')
    return df
