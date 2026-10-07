import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.config.settings import CLEANED_DIR, PROCESSED_DIR, FIG_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_eda():
    logger.info('Starting EDA and Figure Generation')
    
    sns.set_theme(style='whitegrid')
    
    # Data Science Jobs
    ds_path = CLEANED_DIR / 'cleaned_ds_jobs.csv'
    if ds_path.exists():
        ds = pd.read_csv(ds_path)
        plt.figure(figsize=(10,6))
        sns.barplot(data=ds.sort_values('num_of_jobs', ascending=False).head(10), y='job_title', x='num_of_jobs')
        plt.title('Top Data Science Roles by Volume')
        plt.tight_layout()
        plt.savefig(FIG_DIR / 'ds_roles_volume.png')
        plt.close()
        
    # JDS
    jds_path = CLEANED_DIR / 'cleaned_jds.csv'
    if jds_path.exists():
        jds = pd.read_csv(jds_path)
        plt.figure(figsize=(10,6))
        sns.boxplot(data=jds.melt(id_vars=['target', 'id']), x='value', y='variable', hue='target')
        plt.title('JDS Skill Distributions by Outcome')
        plt.tight_layout()
        plt.savefig(FIG_DIR / 'jds_skills_boxplot.png')
        plt.close()
        
    # SDS
    sds_path = CLEANED_DIR / 'cleaned_sds.csv'
    if sds_path.exists():
        sds = pd.read_csv(sds_path)
        plt.figure(figsize=(10,6))
        sns.boxplot(data=sds.melt(id_vars=['target', 'id']), x='value', y='variable', hue='target')
        plt.title('SDS Trait Distributions by Outcome')
        plt.tight_layout()
        plt.savefig(FIG_DIR / 'sds_traits_boxplot.png')
        plt.close()
        
    logger.info('EDA Complete.')
