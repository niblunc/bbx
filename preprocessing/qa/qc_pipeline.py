

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


# get scan notes
df_w1_notes=pd.read_csv('w1_notes.csv', encoding='latin-1')
#df_w1_notes.head()
#df_w1_notes.columns
df_clean=df_w1_notes[['participantID', 'w1scan_scannotes']]

df_clean.set_index("participantID", inplace=True)
df_clean.index = df_clean.index.str.lower()
df_clean = df_clean.drop(['participant id (bbx_###)'])

# Step 1: Given an expected range (i.e 1-50), list DICOM subjects not found in that range.

# Get DICOM id list
s1_dcms = [x.split("/")[-1].split("-")[1].lstrip("0") for x in
             glob.glob(os.path.join(bids_path, "sourcedata/DICOM/ses-1/sub-*"))]
s1_dcms = np.unique(np.array(s1_dcms)).tolist()
# get expected id list from notes
s1_sub_ids = sorted([x.split("_")[1].lstrip('0') for x in df_clean.index.values])
s1_sub_ids = np.unique(np.array(s1_sub_ids)).tolist()

# get total count for DICOM and expected id lists
s1_sub_exp_ct = len(s1_sub_ids)
s1_sub_dcm_ct = len(s1_dcms)

# return the unique values in ar1 that are not in ar2
# ids found in dicom directory but not id list
s1_mia_id = np.setdiff1d(s1_dcms, s1_sub_ids)

# ids missing from dicom directories
s1_mia_dcm = np.setdiff1d(s1_sub_id_lst, s1_dcms)

s1_mia_id = s1_mia_id.tolist()
s1_mia_dcm = s1_mia_dcm.tolist()

# look at scan notes for any missing DICOM ids
for id_ in s1_mia_dcm:
    bbx_id = "bbx_{:03d}".format(int(id_))
    try:
        print("{}, notes: \n{}".format(bbx_id, df_clean.loc[bbx_id]))
    except:
        print("Missing scan notes for ", bbx_id)

## Report Output
print("\nExpected subject count: {} \tUnique DICOM directories found: {}".format(s1_sub_exp_ct, s1_sub_dcm_ct))
print("\nMissing DICOM directories for IDs: {} \n\nMissing scan note IDs, but found DICOM directories: {} \n".format(s1_mia_dcm, s1_mia_id))




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
