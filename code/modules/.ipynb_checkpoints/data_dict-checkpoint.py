import os, glob
import pandas as pd
from IPython.display import display


"""
# BBX Data Dictionary Build Program
# by Nichollette Acosta

## Program takes in raw behavioral files (.tsv)

"""

class DataDict():

    def __init__(self, data_path):
        self.data_path=data_path

    def load_data(self):
        data_path=self.data_path
        print('[INFO] data path %s'%self.data_path)
        behav_df = pd.read_csv(os.path.join(data_path, "bbx_w1behav_raw_09242020.csv"))
        clean_df = pd.read_excel(os.path.join(data_path,  "bbx_w1behav_cleandata_082819.xlsx"))
        display(behav_df)
        display(clean_df)
        
        
    def 

#clean_df

data_folder='/Users/nikkibytes/Documents/git_nibl/bbx/data/behavioral/data_dict'

test= DataDict(data_folder)
test.load_data()