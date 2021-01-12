import os, glob
import pandas as pd
from IPython.display import display


"""
# BBX Calculations
# by Nichollette Acosta

## Program takes in raw behavioral files (.tsv)

"""

class DataDict():

    def __init__(self, data_path):
        self.data_path=data_path

    def load_data(self):
        """
        """
        data_path=self.data_path
        #print('[INFO] data path %s'%self.data_path)
        #behav_df = pd.read_csv(os.path.join(data_path, "bbx_msBxScn_datadict_12_30_20.xlsx"))
        df = pd.read_excel(os.path.join(data_path,  "bbx_msBxScn_datadict_12_30_20.xlsx"), sheet_name='scoring')
        #display(df)
        #print(df.columns.values)
        
    def ffq_calculation():
        """
        """
        
        
    
def test():
    """
    test() method 
    """
    data_folder='C:\\Users\\19802\\Documents\\nibl'
    s1_behavioral=(os.path.join(data_path, "bbx_w1_msBxScn_01_06_21.tsv"))
    test= DataDict(data_folder)
    test.load_data()

"""
# inputs expected
# data folder
# datafile mainly

"""