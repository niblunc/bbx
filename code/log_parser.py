"""
@author: NTA, at NIBL
The module is used to parse log files from the bbx experiment
"""
import os, glob
import pandas as pd
from IPython.display import display



# Module
class OnsetSetup():

    def __init__(self, folder_path):
        self.folder_path=folder_path
        self.onset_dict={}

    def get_files(self):
        log_file_list=glob.glob(os.path.join(self.folder_path, "*.log"))
        log_file_list.sort()
        return log_file_list;

    def load_file(self, file):
        onset_dict=self.onset_dict
        sub_id=file.split('/')[-1].split("_")[1]
        run=file.split('/')[-1].split("_")[2]
        wave=file.split('/')[-1].split("_")[3]

        if "pre" in wave or "post" in wave:
            if sub_id not in onset_dict:
                onset_dict[sub_id]={
                    "SSBCUE": [],
                    "USBCUE": [],
                    "H2OCUE": [],
                    "SSBTASTE": [],
                    "USBTASTE": [],
                    "H2OTASTE": [],
                    "NEU": [],
                    "START TIME": None
                }

            df=pd.read_csv(file, sep="\t", header=None)
            df.columns =["time", "string1", "string2"]
            #print(sub_id, run, wave)
            #display(df)
            print(df['string1'].unique())

            # find start time rows
            #print("[INFO] querying start time....")
            st_query=df.query('string1 in "Level start key press "')
            #display(st_query)
            onset_dict[sub_id]["START TIME"] = st_query

            # SSB: cue and taste query
            # The SSBs are  either "C0" or "SL"
            # -- no one will receive both
            ssb_cue_query=df[df["string1"].str.contains("image=CO.jpg")]
            display(ssb_cue_query)
            ssb_cue_query = df[df["string1"].str.contains("image=CO.jpg")]
            display(ssb_cue_query)
            onset_dict[sub_id]["SSBCUE"] = ssb_cue_query
            # ssb taste --

            # USB: cue and taste query

            # Water: cue and taste

            # Neutral ~ rinse


        else:
            pass


        self.onset_dict=onset_dict

# Test Cases

def test_data_grab(obj):
    log_files=obj.get_files()
    #print("[INFO] found %s log files. \n %s"%(len(log_files), log_files[:3]))
    return log_files;

def test_file_load(obj, log_files):
    for file in log_files[:5]:
        obj.load_file(file)



# Main -- user must run
# set variables and initialize object
data_folder="/Users/nikkibytes/Documents/local_dev/bbx/log_files"
obj=OnsetSetup(data_folder)
log_files=test_data_grab(obj)
test_file_load(obj, log_files)


