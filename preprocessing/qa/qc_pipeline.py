

import glob, os
import pandas as pd
import pdb
from IPython.core import display as ICD
pd.options.display.max_rows
pd.set_option('display.max_colwidth', -1)
import numpy as np



# Load data:

# setup available paths
bids_path = '/projects/niblab/bids_projects/Experiments/bbx/bids/'

# get expected range
range_val = 159 #input("Expected subject range: ")
expected_sub_lst=list(range(1,int(range_val))) # Expecting subject IDs 1-56

# get scan notes
df_w1_notes=pd.read_csv('w1_notes.csv', encoding='latin-1')
#df_w1_notes.head()
#df_w1_notes.columns
df_clean=df_w1_notes[['participantID', 'w1scan_scannotes']]


# Step 1: Given an expected range (i.e 1-50), list DICOM subjects not found in that range.
excluded_subjects = []
s1_dcms = [x.split("/")[-1].split("-")[1].lstrip("0") for x in
             glob.glob(os.path.join(bids_path, "sourcedata/DICOM/ses-1/sub-*"))]
s2_dcms = [x.split("/")[-1].split("-")[1].lstrip("0") for x in
             glob.glob(os.path.join(bids_path, "sourcedata/DICOM/ses-2/sub-*"))]

s1_mia = np.setdiff1d(expected_sub_lst,s1_dcms)
s2_mia = np.setdiff1d(expected_sub_lst,s2_dcms)
s1_mia= s1_mia.tolist()
s2_mia= s2_mia.tolist()

## loop through missing ids and see if any notes are found, add to drop list of not found.
s1_drop_list = []
s2_drop_list = []

for id_ in s1_mia:
    bbx_id = "bbx_{:03d}".format(id_)
    if df_clean.loc[df_clean['participantID'] == bbx_id].empty:
        print("Subject, {}, has no scan notes available, inferring then the scan did not take place, and subject is dropped.".format(bbx_id))

        s1_mia.remove(id_)
    else:
        print("Subject, {}, notes: \n{}".format(bbx_id, df_clean.loc[df_clean['participantID'] == bbx_id]))



print("> MISSING DICOMS: \nS1: {} \t\tS2: {} \nS1 MISSING SUBJECTS: {} \nS2 MISSING SUBJECTS: {} ".format(len(s1_mia), len(s2_mia), s1_mia, s2_mia))



# What subjects haven't been translated to BIDS?


s1_bids = [x.split("/")[-2].split("-")[1].lstrip("0") for x in
             glob.glob(os.path.join(bids_path, "sub-*/ses-1"))]
s2_bids = [x.split("/")[-2].split("-")[1].lstrip("0") for x in
             glob.glob(os.path.join(bids_path, "sub-*/ses-2"))]

s1_mia = np.setdiff1d(s1_dcms, s1_bids)
s2_mia = np.setdiff1d(s2_dcms, s2_bids)


print("> SUBJECTS NOT AVAIlABLE IN BIDS: \nS1: {} \tS2: {} \nS1 SUBJECTS MISISNG: {} \nS2 SUBJECTS MISSING: {}".format(len(s1_mia), len(s2_mia), s1_mia, s2_mia))



# Subjects missing from fmriprep?

s1_fprep = [x.split("/")[-2].split("-")[1].lstrip("0") for x in
              glob.glob(os.path.join(bids_path, "derivatives/fmriprep/sub-*/ses-1"))]
s2_fprep = [x.split("/")[-2].split("-")[1].lstrip("0") for x in
              glob.glob(os.path.join(bids_path, "derivatives/fmriprepsub-*/ses-2"))]

s1_mia = np.setdiff1d(s1_bids, s1_fprep)
s2_mia = np.setdiff1d(s2_bids, s2_fprep)

print("> SUBJECTS NOT AVAIlABLE IN FMRIPREP: \nS1: {} \tS2: {} \nS1 SUBJECTS MISSING: \t{} \nS2 SUBJECTS MISSING: \t{} ".format(len(s1_mia), len(s2_mia), sorted(s1_mia), sorted(s2_mia)))
