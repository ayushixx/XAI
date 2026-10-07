import pandas as pd
from src.config.settings import RAW_DIR, CLEANED_DIR, FILE_MAPPING
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_sds():
    logger.info('Cleaning SDS dataset')
    filepath = RAW_DIR / FILE_MAPPING['sds']
    if not filepath.exists():
        return None
    df = pd.read_excel(filepath)
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '')
    
    target_col = 'success_classification_high_low'
    if target_col in df.columns:
        df['target'] = df[target_col].apply(lambda x: int(x) if str(x).strip() in ['0', '1'] else (1 if str(x).lower().strip() == 'high' else 0))
        
    df.to_csv(CLEANED_DIR / 'cleaned_sds.csv', index=False)
    logger.info(f'Cleaned SDS: {len(df)} rows remain.')
    return df
