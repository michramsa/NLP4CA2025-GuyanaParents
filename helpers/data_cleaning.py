# Topic Modelling for the People - https://maria-antoniak.github.io/2022/07/27/topic-modeling-for-the-people.html
# Some important notes about this - we may not necessarily be able to follow some of these rules completely because we're dealing
# with data that may contain all English, all Creolese, or a mix of English and Creolese. 

### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

# data has text called [deleted], which are unneeded 
def remove_deleted(csv):
    df = pd.read_csv(csv)
    print(df.head())

if __name__=="__main__":
    # test function
    remove_deleted(raw_data_file)