import pandas as pd
from src.config.settings import RAW_DIR, CLEANED_DIR, FILE_MAPPING
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_jds():
    logger.info('Cleaning JDS dataset')
    filepath = RAW_DIR / FILE_MAPPING['jds']
    if not filepath.exists():
        return None
    df = pd.read_excel(filepath)
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '')
    df = df.dropna(how='all')
    
    target_col = 'salary_hike_high_or_low'
    if target_col in df.columns:
        df['target'] = df[target_col].apply(lambda x: int(x) if str(x).strip() in ['0', '1'] else (1 if str(x).lower().strip() == 'high' else 0))
    
    df.to_csv(CLEANED_DIR / 'cleaned_jds.csv', index=False)
    logger.info(f'Cleaned JDS: {len(df)} rows remain.')
    return df
