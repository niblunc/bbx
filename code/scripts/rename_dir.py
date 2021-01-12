import os, glob

import shutil

dir_base ='/projects/niblab/bids_projects/Experiments/bbx/bids/sourcedata/DICOM'
dir_list=glob.glob(os.path.join(dir_base, "Bbx_*"))

for dir_path in dir_list:
    #print(dir_path)
    filename_orig=dir_path.split("/")[-1]
    sub_id = filename_orig.split("_")[1].lower()
    sess_id = filename_orig.split("_")[2]
    print(sub_id, sess_id)
    if sess_id == "W1": #session-1
        new_path = os.path.join(dir_base, "ses-1", sub_id)
    else:
        new_path = os.path.join(dir_base, "ses-2", sub_id)
    shutil.move(dir_path, new_path)
    print(dir_path, new_path)