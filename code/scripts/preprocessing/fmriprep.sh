#!/bin/bash
#SBATCH --job-name=fMRIbbx
#SBATCH -t 24:00:00
#SBATCH --mem-per-cpu 80000
## %A == SLURM_ARRAY_JOB_ID
## %a == SLURM_ARRAY_TASK_ID
#SBATCH -o /projects/niblab/bids_projects/Experiments/bbx/bids/code/fmriprep/error_files/asym_%a_fprep_out.txt
#SBATCH -e /projects/niblab/bids_projects/Experiments/bbx/bids/code/fmriprep/error_files/asym_%a_fprep_err.txt

if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then
    id="00${SLURM_ARRAY_TASK_ID}"
elif [ ${SLURM_ARRAY_TASK_ID} -lt 100 ]; then
    id="0${SLURM_ARRAY_TASK_ID}"
else
    id="${SLURM_ARRAY_TASK_ID}"
fi


singularity exec -B /projects/niblab/bids_projects:/base_dir -B /projects/niblab/bids_projects/mytemplateflowdir:/opt/templateflow /projects/niblab/bids_projects/Singularity_Containers/fmriprep_v2_2019.simg \
fmriprep /base_dir/Experiments/bbx/bids /base_dir/Experiments/bbx/bids/derivatives/fmriprep \
    participant  \
    --participant-label ${id} \
    --skip_bids_validation \
    --fs-license-file /base_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --longitudinal \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming \
    --bold2t1w-dof 12 --fd-spike-threshold 0.9 \
    --output-spaces MNI152NLin2009cAsym \
     -w /base_dir/Experiments/bbx/bids/derivatives/fmriprep/fmriprep_wf \
     --resource-monitor --stop-on-first-crash