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

    def load_file(self, file, output_path):
        sub_id=file.split('/')[-1].split("_")[1]
        run=file.split('/')[-1].split("_")[2].split("0")[1]
        wave=file.split('/')[-1].split("_")[3]

        if "pre" in wave or "post" in wave:
            if "post" in wave:
                ses = 'ses-2'
            if wave == "pre":
                ses = 'ses-1'
            #print(sub_id, run, ses)


            logf_df=pd.read_csv(file, sep="\t", header=None)
            logf_df.columns =["time", "data", "keypress"]

            # Set Start time dataframes
            #print("[INFO] querying start time....")
            st_query=df[df['string1'].str.contains('Level start key press')]
            display(st_query)
            start_time=int(st_query['time'])

            # SSB: cue and taste query
            # The SSBs are  either "C0" or "SL"
            # -- no one will receive both
            ssb_cue_query=df[(df["string1"].str.contains("image=CO.jpg")) | (df["string1"].str.contains("image=SL.jpg"))]
            ssb_cue_query= ssb_cue_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            ssb_cue_query["stim"] = 6
            ssb_cue_query["mod"] = 1
            # subtract start time
            ssb_cue_query.time = ssb_cue_query.time - start_time
            ssb_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "SSBcue", run))
            print('[INFO] SSBcue: ', ssb_cue_tsv)
            ssb_cue_query.to_csv(ssb_cue_tsv, sep="\t", index=False, header=False)

            ssb_taste_query = df[df["string1"].str.contains("Level post injecting via pump at address 1")]
            ssb_taste_query = ssb_taste_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            ssb_taste_query["stim"] = 6
            ssb_taste_query["mod"] = 1
            # subtract start time
            ssb_taste_query.time = ssb_taste_query.time - start_time
            ssb_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "SSBtaste", run))
            print('[INFO] SSBtaste: ', ssb_taste_tsv)
            ssb_taste_query.to_csv(ssb_taste_tsv, sep="\t", index=False, header=False)

            # USB: cue and taste query
            usb_cue_query = df[(df["string1"].str.contains("image=UCO.jpg")) | (df["string1"].str.contains("image=USL.jpg"))]
            usb_cue_query = usb_cue_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            usb_cue_query["stim"] = 1
            usb_cue_query["mod"] = 1
            # subtract start time
            usb_cue_query.time = usb_cue_query.time - start_time
            usb_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "USBcue", run))
            print('[INFO] USBcue: ',usb_cue_tsv)
            usb_cue_query.to_csv(usb_cue_tsv, sep="\t", index=False, header=False)

            usb_taste_query = df[df["string1"].str.contains("Level post injecting via pump at address 2")]
            usb_taste_query = usb_taste_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            usb_taste_query["stim"] = 6
            usb_taste_query["mod"] = 1
            # subtract start time
            usb_taste_query.time = usb_taste_query.time - start_time
            usb_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "USBtaste", run))
            print('[INFO] USB taste: ',usb_taste_tsv)
            usb_taste_query.to_csv(usb_taste_tsv, sep="\t", index=False, header=False)


            # Water: cue and taste
            h2O_cue_query = df[(df["string1"].str.contains("image=water.jpg"))]
            h2O_cue_query = h2O_cue_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            h2O_cue_query["stim"] = 6
            h2O_cue_query["mod"] = 1
            # subtract start time
            h2O_cue_query.time = h2O_cue_query.time - start_time
            h2O_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "h2Ocue", run))
            print('[INFO] h2O cue: ',h2O_cue_tsv)
            h2O_cue_query.to_csv(h2O_cue_tsv, sep="\t", index=False, header=False)


            h2O_taste_query = df[df["string1"].str.contains("Level post injecting via pump at address 0")]
            h2O_taste_query = h2O_taste_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            h2O_taste_query["stim"] = 6
            h2O_taste_query["mod"] = 1
            # subtract start time
            h2O_taste_query.time = h2O_taste_query.time - start_time
            h2O_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv" % (sub_id, ses, "h2Otaste", run))
            print('[INFO] h2O taste: ',h2O_taste_tsv)
            h2O_taste_query.to_csv(h2O_taste_tsv, sep="\t", index=False, header=False)

            # Neutral ~ rinse
            neu_query = df[(df["string1"].str.contains("Level RINSE"))]
            neu_query = neu_query.drop(["string1", "string2"], axis=1)
            # add stim time and mod column
            neu_query["stim"]=6
            neu_query["mod"] = 1
            # subtract start time
            neu_query.time=neu_query.time-start_time
            # write to file
            neu_tsv=os.path.join(output_path, "sub-%s_%s_task-%s_run-%s.tsv"%(sub_id, ses, "neu", run))
            print('[INFO] neutral/rinse: ',neu_tsv)
            neu_query.to_csv(neu_tsv, sep="\t", index=False, header=False)


        else:
            pass



# Test Cases

def test_data_grab(obj):
    log_files=obj.get_files()
    #print("[INFO] found %s log files. \n %s"%(len(log_files), log_files[:3]))
    return log_files;

def test_file_load(obj, log_files):
    output_path='/Users/nikkibytes/Documents/local_dev/bbx/output_onsets'
    for file in log_files:
        obj.load_file(file, output_path)



# Main -- user must run
# set variables and initialize object
data_folder="/Users/nikkibytes/Documents/local_dev/bbx/log_files"
obj=OnsetSetup(data_folder)
log_files=test_data_grab(obj)
test_file_load(obj, log_files)


