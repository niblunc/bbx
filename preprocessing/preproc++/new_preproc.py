import os, glob
import pandas as pd
import subprocess



def fd_check():
    #sub-001_ses-1_task-training_run-4_desc-confounds_regressors.tsv
    fmriprep_dir ='/Users/nikkibytes/Documents/git_nibl/data/bbx_test_data/bids/dervatives/fmriprep/sub-001/ses-1/func/'
    confound_file=os.path.join(fmriprep_dir,'sub-001_ses-1_task-training_run-4_desc-confounds_regressors.tsv' )
    nifti = os.path.join(fmriprep_dir,'sub-001_ses-1_task-training_run-4_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
    confound_df = pd.read_csv(confound_file, '\t')
    #print(confound_df.columns.values)
    frame_displace = confound_df['framewise_displacement']
    print(frame_displace)
    nvols_cmd = "fslnvols " + nifti
    volume = subprocess.check_output(nvols_cmd, shell=True, encoding="utf-8")
    volume = volume.strip()
    comparator = int(volume) * .25
    print(comparator)


def main():
    tsv_file = '/Users/nikkibytes/Documents/git_nibl/bbx/bbx_scan_QC.tsv'
    print(tsv_file)
    fd_check()
main()