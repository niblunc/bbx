#!/bin/bash
#
#SBATCH --job-name=bbxbids
#SBATCH -N 1
#SBATCH -c 1
#SBATCH -t 2:00:00
## %A == SLURM_ARRAY_JOB_ID
## %a == SLURM_ARRAY_TASK_ID
#SBATCH -o /projects/niblab/bids_projects/Experiments/bbx/bids/code/bids/error_files/bids_%a_out.txt
#SBATCH -e /projects/niblab/bids_projects/Experiments/bbx/bids/code/bids/error_files/bids_%a_err.txt

if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then
    id="00${SLURM_ARRAY_TASK_ID}"
elif [ ${SLURM_ARRAY_TASK_ID} -lt 100 ]; then
    id="0${SLURM_ARRAY_TASK_ID}"
else
    id="${SLURM_ARRAY_TASK_ID}"
fi

singularity exec -B /:/base_dir /projects/niblab/bids_projects/Singularity_Containers/heudiconv_05_2019.simg \
heudiconv -b -d /base_dir/projects/niblab/bids_projects/Experiments/bbx/bids/sourcedata/DICOM/ses-{session}/sub-{subject}/*dcm -s $id -ss $1 \
-f /base_dir/projects/niblab/bids_projects/Experiments/bbx/bids/code/bbx_heuristic.py \
-c dcm2niix -o /base_dir/projects/niblab/bids_projects/Experiments/bbx/bids