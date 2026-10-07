import pandas as pd
from src.config.settings import RAW_DIR, AUDIT_DIR, FILE_MAPPING, REPORTS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def discover_and_inventory():
    logger.info('Starting Phase 1 & 2: File Discovery & Data Inventory')
    inventory = []
    
    for key, filename in FILE_MAPPING.items():
        filepath = RAW_DIR / filename
        if not filepath.exists():
            logger.warning(f'MISSING DATASET: {filename}')
            continue
            
        logger.info(f'Discovered dataset: {filename}')
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
            
        for col in df.columns:
            inventory.append({
                'dataset': key,
                'filename': filename,
                'rows': len(df),
                'columns': len(df.columns),
                'column_name': col,
                'data_type': str(df[col].dtype),
                'missing_values': df[col].isnull().sum(),
                'missing_percentage': df[col].isnull().sum() / len(df) * 100,
                'unique_values': df[col].nunique(),
                'min': df[col].min() if pd.api.types.is_numeric_dtype(df[col]) else None,
                'max': df[col].max() if pd.api.types.is_numeric_dtype(df[col]) else None,
                'mean': df[col].mean() if pd.api.types.is_numeric_dtype(df[col]) else None,
                'median': df[col].median() if pd.api.types.is_numeric_dtype(df[col]) else None,
                'std': df[col].std() if pd.api.types.is_numeric_dtype(df[col]) else None,
            })
            
    inv_df = pd.DataFrame(inventory)
    inv_df.to_csv(AUDIT_DIR / 'data_inventory.csv', index=False)
    
    with open(REPORTS_DIR / 'audit' / 'data_inventory.md', 'w') as f:
        f.write('# Data Inventory\\n\\n')
        f.write(inv_df[['dataset', 'rows', 'columns']].drop_duplicates().to_markdown(index=False))
        f.write('\\n\\n')
        f.write(inv_df.to_markdown(index=False))
        
    logger.info('Inventory complete.')
    return inv_df
