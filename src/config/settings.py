from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
AUDIT_DIR = DATA_DIR / 'audit'
CLEANED_DIR = DATA_DIR / 'cleaned'
PROCESSED_DIR = DATA_DIR / 'processed'
OUTPUTS_DIR = DATA_DIR / 'outputs'
SAS_DIR = OUTPUTS_DIR / 'sas'
MODELS_DIR = BASE_DIR / 'models'
REPORTS_DIR = BASE_DIR / 'reports'
FIG_DIR = REPORTS_DIR / 'figures'

FILE_MAPPING = {
    'ds_jobs': 'DataScience Jobs.csv',
    'analytics_jobs': 'Analytics Jobs.csv',
    'jds': 'JDS Skill Traits.xlsx',
    'sds': 'SDS Personality Traits.xlsx'
}
