import os, glob
path_onsets = "/projects/niblab/bids_projects/Experiments/bbx/clean_onsets"

text_files=glob.glob(os.path.join(path_onsets, "*.txt"))

for file_path in text_files:
    file = file_path.split("/")[-1]
    task = file.split("_")[2].split("-")[1]
    ##print(task)
    if task == "Tcue":
        new_name=file_path.replace(task, "SSBcue")
        print('renaming {} to {} '.format(file_path,new_name))
    elif task == "Ucue":
        new_name=file_path.replace(task, "USBcue")
        print('renaming {} to {} '.format(file_path,new_name))
    elif task == "Ncue":
        new_name=file_path.replace(task, "H2Ocue")
        print('renaming {} to {} '.format(file_path,new_name))
    elif task == "TT":
        new_name=file_path.replace(task, "SSBtaste")
        print('renaming {} to {} '.format(file_path,new_name))
    elif task == "UU":
        new_name=file_oath.replace(task, "USBtaste")
        print('renaming {} to {} '.format(file_path,new_name))
    elif task == "NN":
        new_name=file_path.replace(task, "H2Otaste")
        print('renaming {} to {} '.format(file_path,new_name))

    else:
        pass


path_onsets = "/projects/niblab/onesets_staging/onsets2"
text_files=glob.glob(os.path.join(path_onsets, "*.txt"))
# bbx_run03_UU_152.txt --> sub-019_ses-2_task-WW_run-2.txt
for file_path in text_files:
    file = file_path.split("/")[-1]
    task = file.split("_")[2]
    subject_id = "sub-"+file.split("_")[3].split(".")[0]
    run_id = file.split("_")[1]
    run_id = run_id.replace("0", "-")

    if task == "Tcue":
        new_name="{}_task-SSBcue_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path, new_path))
        os.rename(file_path, new_path)
    elif task == "Ucue":
        new_name = "{}_task-USBcue_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path, new_path))
        os.rename(file_path, new_path)
    elif task == "Ncue":
        new_name = "{}_task-H2Ocue_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path, new_path))
        os.rename(file_path, new_path)
    elif task == "TT":
        new_name = "{}_task-SSBtaste_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path, new_path))
        os.rename(file_path, new_path)
    elif task == "UU":
        new_name = "{}_task-USBtaste_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path, new_path))
        os.rename(file_path, new_path)
    elif task == "NN":
        new_name = "{}_task-H2Otaste_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path,new_path))
        os.rename(file_path, new_path)
    elif task == "rinse":
        new_name = "{}_task-rinse_{}.txt".format(subject_id, run_id)
        new_path = os.path.join(path_onsets, new_name)
        print('renaming {} to {} '.format(file_path,new_path))
        os.rename(file_path, new_path)
    else:
        pass