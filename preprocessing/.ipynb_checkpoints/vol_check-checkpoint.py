# Script for building quality check for BIDS

import os, glob
import pandas as pd
import subprocess


def dict_make(sessions, sub_dirs):
    qa_dict = {}
    vol_dict = {}
    # loop through each sessions we have
    outfile=open("/projects/niblab/bids_projects/Experiments/bbx/bids/derivatives/bad_volumes.txt", 'w')
    for sess_id in sessions:
        if sess_id not in qa_dict:
            qa_dict[sess_id] = {}
        if sess_id not in vol_dict:
            vol_dict[sess_id] = {}
        # loop through subjects by their bids path
        for sub_path in sorted(sub_dirs):
            base_dir = os.path.join(sub_path, sess_id)
            sub_id = sub_path.split("/")[-1]
            if sub_id not in qa_dict[sess_id]:
                if sess_id == "ses-1":
                    qa_dict[sess_id][sub_id] = { "func": None, "runs_train": None, "runs_rest": None, "anat": None, "fmap": None }
                else:
                    qa_dict[sess_id][sub_id] = { "func": None, "runs_rl": None, "runs_train": None, "runs_rest": None, "anat": None, "fmap": None }

            # Functional files: func/
            funcs_nii=glob.glob("/projects/niblab/bids_projects/Experiments/bbx/bids/{}/{}/func/*.nii.gz".format(sub_id, sess_id))
            #print(funcs_nii)
            bad_funcs = []

            # add values to qa_dict -
            nii_ct = len(funcs_nii)
            qa_dict[sess_id][sub_id]["func"] = nii_ct
            qa_dict[sess_id][sub_id]["runs_train"] = len([x for x in funcs_nii if "training" in x])
            qa_dict[sess_id][sub_id]["runs_rest"] = len([x for x in funcs_nii if "resting" in x])

            if sess_id == "ses-2":
                qa_dict[sess_id][sub_id]["runs_rl"] = len([x for x in funcs_nii if "rl_" in x])

            # volume check -
            for func in funcs_nii:

                filename=func.split("/")[-1]
                task=func.split("/")[-1].split("_")[2]
                if task != "resting":
                    run_id = func.split('/')[-1].split('_')[3]
                else:
                    run_id = None
                fsl_cmd ="fslnvols {}".format(func)
                vol=subprocess.check_output(fsl_cmd, shell=True)
                vol=str(vol,'utf-8').strip()

                if "training" in task:
                    expected_vol = 233
                elif "rl" in task:
                    expected_vol = 212
                else:
                    expected_vol = 147
                if int(vol) != expected_vol:
                    #print("File:{} \t\t Volume:{}".format(filename, vol))
                    temp_tuple=(filename, vol)
                    #print("Found bad functional file...........")
                    if "training" in task:
                        line="File:{} \t Volume:{}".format(filename, vol)
                    else:
                        line="File:{} \t\t Volume:{}".format(filename, vol)
                    #print(line)
                    outfile.write(line+"\n")

                    bad_funcs.append(temp_tuple)


            # if we found bad files, do something with them here
            if bad_funcs:
                #print("ID:{} \t {}".format(sub_id,bad_funcs))
                if sub_id not in vol_dict[sess_id]:
                    vol_dict[sess_id][sub_id] = {}
                vol_dict[sess_id][sub_id]["FILES"] = bad_funcs

            # Anatomical files: anat/
            anat_nii=glob.glob("/projects/niblab/bids_projects/Experiments/bbx/bids/{}/{}/anat/*.nii.gz".format(sub_id, sess_id))
            #print(anat_nii)
            # add value to dict-
            nii_ct = len(anat_nii)
            qa_dict[sess_id][sub_id]["anat"] = nii_ct

            # Field mapping files: fmap/
            fmap_nii=glob.glob("/projects/niblab/bids_projects/Experiments/bbx/bids/{}/{}/func/*.nii.gz".format(sub_id, sess_id))
            #print(fmap_nii)
            # add value to dict-
            nii_ct = len(fmap_nii)
            qa_dict[sess_id][sub_id]["fmap"] = nii_ct

    #print("SESSION {} DICTIONARY: \n{}\n".format(sess_id,qa_dict[sess_id]))
    #print(vol_dict)
    outfile.close()
    return qa_dict


def analyze_data(qa_dict):
    for sess_id in qa_dict:
        zero_df = pd.DataFrame()
        partial_df = pd.DataFrame()
        no_zero_df = pd.DataFrame()


        print(">>> {}.......".format(sess_id))
        df = pd.DataFrame(qa_dict[sess_id])
        #print(df.head())
        #df.T.to_csv("bro_bids_{}.csv".format(sess_id), sep="\t")

        for sub_id in df.columns:
            #zero=df[sub_id] == 0

            all_zero=(df[sub_id]==0).all()
            any_zero=(df[sub_id]==0).any()

            if all_zero == True:
                zero_df[sub_id] = df[sub_id]
            elif any_zero == True:
                partial_df[sub_id] = df[sub_id]
            else: # should have all numbers
                no_zero_df[sub_id] = df[sub_id]

        print(zero_df)
        print(partial_df)
        print(no_zero_df)
        filename="/projects/niblab/bids_projects/Experiments/bbx/bids/derivatives/bbx_{}_".format(sess_id)
        zero_df.T.to_csv(filename+"missing.csv", sep="\t")
        partial_df.T.to_csv(filename+"partial_missing.csv", sep="\t")
        no_zero_df.T.to_csv(filename+"found.csv", sep="\t")
        #print('Zero files found list: {} \nSome missing files list: {} \nAll files found:{} \n'.format(all_lst, partial_lst, no_z_lst))

def main():
    # get paths and subject directory paths
    BIDS_PATH = "/projects/niblab/bids_projects/Experiments/bbx/bids"
    sub_dirs = glob.glob(os.path.join(BIDS_PATH, 'sub-*'))
    #print(sub_dirs)
    # get the multiple sessions
    sessions=['ses-1',"ses-2"]
    qa_dict = dict_make(sessions, sub_dirs)
    analyze_data(qa_dict)
main()
