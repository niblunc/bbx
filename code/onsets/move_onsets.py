import glob, os
from shutil import copy2

onset_dir = '/projects/niblab/bids_projects/Experiments/bbx/clean_onsets'

deriv_dir = '/projects/niblab/bids_projects/Experiments/bbx/bids/derivatives'

onsets=sorted(glob.glob(os.path.join(onset_dir, "*.txt")))

for onset in onsets:
    sub_id = onset.split("/")[-1].split("_")[0]
    #print(sub_id)
    new_path=os.path.join(deriv_dir, sub_id, "func/onsets")
    #print(new_path)
    if not os.path.exists(new_path):
        #print('not exists')
        os.makedirs(new_path)
    print("moving {} into {}".format(onset, new_path))
    copy2(onset, new_path)

onset_dir2 = '/projects/niblab/onesets_staging/onsets2'
onsets2=sorted(glob.glob(os.path.join(onset_dir2, "*.txt")))

for onset in onsets2:
    sub_id = onset.split("/")[-1].split("_")[0]

    print(sub_id.rjust(3, '0'))
    new_path = os.path.join(deriv_dir, sub_id, "func/onsets")
    print(new_path)
    if not os.path.exists(new_path):
        # print('not exists')
        os.makedirs(new_path)
    print("moving {} into {}".format(onset, new_path))
    copy2(onset, new_path)

