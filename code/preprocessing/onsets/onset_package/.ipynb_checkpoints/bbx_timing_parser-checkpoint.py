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
    
    def quality_check(self, df):
        display(df)

    def load_file(self, file, output_path, verbose=False, qc=False):
        sub_id=file.split('/')[-1].split("_")[1]
        run=file.split('/')[-1].split("_")[2].split("0")[1]
        wave=file.split('/')[-1].split("_")[3]

        if "pre" in wave or "post" in wave:
            if "post" in wave:
                ses = 'ses-2'
            if wave == "pre":
                ses = 'ses-1'
            
            if verbose==True: print("---")
            if verbose==True: print("[INFO] %s %s run-%s "%(sub_id, ses, run))
            
            try:
            
                # load data

                df=pd.read_csv(file, sep="\t", header=None)
                df.columns =["time", "data", "keypress"]

                # Set start time dataframes
                #if verbose==True: print("[INFO] querying start time....")
                # get start time 
                st_query=df[df['data'].str.contains('Level start key press')]
                start_time=float(st_query['time'])
                if verbose==True: print('[INFO] start time: ', start_time)



                # Grab Onsets- 
                ssb_cue_query=df[(df["data"].str.contains("image=CO.jpg")) | 
                                      (df["data"].str.contains("image=SL.jpg"))]
                ssb_taste_query = df[df["data"].str.contains("Level post injecting via pump at address 1")]
                usb_cue_query = df[(df["data"].str.contains("image=UCO.jpg")) | (df["data"].str.contains("image=USL.jpg"))]
                usb_taste_query = df[df["data"].str.contains("Level post injecting via pump at address 2")]
                h2O_cue_query = df[(df["data"].str.contains("image=water.jpg"))]
                h2O_taste_query = df[df["data"].str.contains("Level post injecting via pump at address 0")]
                neu_query = df[(df["data"].str.contains("Level RINSE"))]

                if verbose ==True: print("\n[INFO] ssbcue query (no mods): \n", ssb_cue_query)
                
                def drop_columns(df):
                    df.drop(["data", "keypress"], axis=1,inplace=True)
                    return df;

                ssb_cue_query=drop_columns(ssb_cue_query)
                usb_cue_query=drop_columns(usb_cue_query)
                h2O_cue_query=drop_columns(h2O_cue_query)
                ssb_taste_query = drop_columns(ssb_taste_query)
                usb_taste_query = drop_columns(usb_taste_query)
                h2O_taste_query = drop_columns(h2O_taste_query)
                neu_query =  drop_columns(neu_query)

                # Add stim and mod columns
                ssb_cue_query["stim"] = 1
                ssb_cue_query["mod"] = 1
                ssb_taste_query["stim"] = 6
                ssb_taste_query["mod"] = 1
                usb_cue_query["stim"] = 1
                usb_cue_query["mod"] = 1
                usb_taste_query["stim"] = 6
                usb_taste_query["mod"] = 1
                h2O_cue_query["stim"] = 1
                h2O_cue_query["mod"] = 1
                h2O_taste_query["stim"] = 6
                h2O_taste_query["mod"] = 1
                neu_query["stim"]=3
                neu_query["mod"] = 1


                if verbose ==True: print("\n[INFO] ssbcue query (mod #2: removed and replaced columns): \n", ssb_cue_query)


                # Subtract start time

                ssb_cue_query.time -=  start_time

                ssb_taste_query.time -= start_time# subtract start time
                usb_cue_query.time -= start_time # subtract start time
                usb_taste_query.time -= start_time# subtract start time
                h2O_cue_query.time -= start_time # subtract start time
                h2O_taste_query.time -= start_time# subtract start time
                neu_query.time -= start_time# subtract start time

                if verbose ==True: print("\n[INFO] ssbcue query (mod #3: subtract start time, %s): \n%s"%(start_time, ssb_cue_query))

                # subtract 4 volumes (8TRS)
                ssb_cue_query.time -=  8
                ssb_taste_query.time -= 8 
                usb_cue_query.time -= 8
                usb_taste_query.time -= 8
                h2O_cue_query.time -= 8 
                h2O_taste_query.time -= 8 # subtract 4 volumes
                neu_query.time -= 8

                if verbose ==True: print("\n[INFO] ssbcue query (mod #4: subtract 4 volumes): \n", ssb_cue_query)



                # Reset Index
                ssb_cue_query.reset_index(inplace=True, drop=True)
                ssb_taste_query.reset_index(inplace=True, drop=True)
                usb_cue_query.reset_index(inplace=True, drop=True)
                #usb_taste_query.reset_index(inplace=True, drop=True)
                h2O_cue_query.reset_index(inplace=True, drop=True)
                #print("[INFO] h2O cue onset setup: \n", h2O_cue_query)
                h2O_taste_query.reset_index(inplace=True, drop=True)
                #print("[INFO] ssb taste onset setup: \n", ssb_taste_query)
                #print("[INFO] ssb cue onset setup: \n", ssb_cue_query)
                neu_query.reset_index(inplace=True, drop=True)



                # Set outfiles
                ssb_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "SSBcue", run))
                ssb_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "SSBtaste", run))
                usb_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "USBcue", run))
                usb_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "USBtaste", run))
                h2O_cue_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "H2Ocue", run))
                h2O_taste_tsv = os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt" % (sub_id, ses, "H2Otaste", run))
                neu_tsv=os.path.join(output_path, "sub-%s_%s_task-%s_run-%s_trimmed.txt"%(sub_id, ses, "rinse", run))

                


                # Write to outfiles
                ssb_cue_query.to_csv(ssb_cue_tsv, sep="\t", index=False, header=False)
                ssb_taste_query.to_csv(ssb_taste_tsv, sep="\t", index=False, header=False)
                usb_cue_query.to_csv(usb_cue_tsv, sep="\t", index=False, header=False)
                usb_taste_query.to_csv(usb_taste_tsv, sep="\t", index=False, header=False)
                h2O_cue_query.to_csv(h2O_cue_tsv, sep="\t", index=False, header=False)
                h2O_taste_query.to_csv(h2O_taste_tsv, sep="\t", index=False, header=False)
                neu_query.to_csv(neu_tsv, sep="\t", index=False, header=False)


                if verbose ==True: print("\n[INFO] ssbcue query (final output): \n", ssb_cue_query)
                if verbose==True: print('\n[INFO] SSBcue: ', ssb_cue_tsv)
                    
                # load dataframe
                new_ssbcue_df=pd.read_csv(ssb_cue_tsv, sep="\t", header=None)
                if verbose ==True: print("\n[INFO] ssbcue output file (loaded as dataframe): \n", new_ssbcue_df)


                #print('[INFO] USB taste: ',usb_taste_tsv)
                #h2O_cue_query = h2O_cue_query.drop(["data", "keypress"], axis=1)
                #print("[INFO] h2O taste onset setup: \n", h2O_taste_query)
                #print('[INFO] h2O taste: ',h2O_taste_tsv)
                #print("[INFO] rinse onset setup: \n", neu_query)            
                #print('[INFO] neutral/rinse: ',neu_tsv)

                if qc==True:
                    self.quality_check(df)
                    
                    
            except Exception as e:
                fileout=os.path.join(output_path, "bbx_onset_errors.txt")
                with open(fileout, 'a') as error_file:
                    error_file.write("%s with error, \n%s"%(file, e))
                    error_file.close()
                print(e)
            
        else:
            pass



