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
ADVANCED_MODELS_DIR = MODELS_DIR / 'advanced'
REPORTS_DIR = BASE_DIR / 'reports'
FIG_DIR = REPORTS_DIR / 'figures'
CONFIG_DIR = BASE_DIR / 'src' / 'config'
CACHE_DIR = DATA_DIR / 'cache'
KG_DIR = DATA_DIR / 'knowledge_graph'
DEMAND_DIR = REPORTS_DIR / 'future_demand'

# Ensure required directories exist
for _d in [MODELS_DIR, ADVANCED_MODELS_DIR, REPORTS_DIR, FIG_DIR, CACHE_DIR, KG_DIR, DEMAND_DIR, SAS_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

FILE_MAPPING = {
    'ds_jobs': 'DataScience Jobs.csv',
    'analytics_jobs': 'Analytics Jobs.csv',
    'jds': 'JDS Skill Traits.xlsx',
    'sds': 'SDS Personality Traits.xlsx'
}

