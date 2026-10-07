import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from src.utils.logger import get_logger
from src.audit.data_inventory import discover_and_inventory
from src.cleaning.clean_data_science_jobs import clean_ds_jobs
from src.cleaning.clean_analytics_jobs import clean_analytics_jobs
from src.cleaning.clean_jds import clean_jds
from src.cleaning.clean_sds import clean_sds
from src.eda.generate_charts import run_eda
from src.statistics.statistical_analysis import run_statistics
from src.modeling.jds_modeling import train_jds
from src.modeling.sds_modeling import train_sds
from src.signal_engine.generate_signals import run_signal_engine

logger = get_logger(__name__)

def main():
    logger.info('=====================================')
    logger.info('8BIT PIPELINE STARTING')
    logger.info('=====================================')
    
    # 1. Discover and Inventory
    discover_and_inventory()
    
    # 2. Clean Datasets
    clean_ds_jobs()
    clean_analytics_jobs()
    clean_jds()
    clean_sds()
    
    # 3. EDA
    run_eda()
    
    # 4. Statistics
    run_statistics()
    
    # 5. Modeling
    train_jds()
    train_sds()
    
    # 6. Signal Engine
    run_signal_engine()
    
    print("\\n=====================================")
    print("8BIT PIPELINE COMPLETE")
    print("=====================================")
    print("Pipeline executed successfully. All models, figures, and exports generated.")
    print("SAS-ready tables available in data/outputs/sas/")

if __name__ == '__main__':
    main()
