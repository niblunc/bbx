
import os, glob
from IPython.core import display as ICD
import pandas as pd
import subprocess
from shutil import copy2

subject_ids = sorted([x.split("/")[-1] for x in
                      glob.glob("/projects/niblab/bids_projects/Experiments/bbx/bids/sub-*")])
print(subject_ids)

deriv_path = "/projects/niblab/bids_projects/Experiments/bbx/bids/derivatives"

for sub_id in subject_ids:
    print("Subject: \t{}".format(sub_id))

    funcs = glob.glob(os.path.join(deriv_path, "{}/ses-1/func/*brain.nii.gz".format(sub_id)))
    for func in sorted(funcs):
        print(func)
        task = func.split("/")[-1].split("_")[2]
        run = func.split("/")[-1].split("_")[3]

        if task != "resting":
            confound_path = os.path.join(deriv_path,
                                         "{}/ses-1/func/motion_assessment/{}_ses-1_{}_{}_confound.txt".format(sub_id,
                                                                                                              sub_id,
                                                                                                              task,
                                                                                                              run))
            outlier_path = os.path.join(deriv_path,
                                        "{}/ses-1/func/motion_assessment/{}_ses-1_{}_{}_outlier_output.txt".format(
                                            sub_id, sub_id, task, run))
        else:
            confound_path = os.path.join(deriv_path,
                                         "{}/ses-1/func/motion_assessment/{}_ses-1_{}".format(sub_id, sub_id, task))
            outlier_path = os.path.join(deriv_path,
                                        "{}/ses-1/func/motion_assessment/{}_ses-1_{}".format(sub_id, sub_id, task))

        outlier_cmd = "fsl_motion_outliers -i %s  -o %s --fd --thresh=0.9 -v > %s" % (func, confound_path, outlier_path)
        subprocess.call(outlier_cmd)
        print(">>> FINISHED {} \n".format(outlier_cmd))
