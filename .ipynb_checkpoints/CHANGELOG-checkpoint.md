# Changelog - bbx
All notable changes to this project will be documented in this file.  


The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added


### Errors
Volume Errors:
- sub-002:  
    - File:sub-002_ses-1_task-training_run-1_bold.nii.gz  		Volume:10  
    - File:sub-002_ses-1_task-training_run-2_bold.nii.gz  		Volume:193  
    *Was able to use two extra runs for replacement*  


- sub-044:  
    - File:sub-044_ses-2_task-resting_bold.nii.gz  		Volume:122  
    *replacement unavailables*  

- sub-048:  
  - File:sub-048_ses-1_task-training_run-1_bold.nii.gz  		Volume:28  
  *replacement unavailable, file removed, remaining files renamed, subject has 3 runs now*  

- sub-077:
  - File:sub-077_ses-1_task-training_run-1_bold.nii.gz  		Volume:9    
  *replacement file was available*

- sub-078:  
  - File:sub-078_ses-1_task-training_run-1_bold.nii.gz  		Volume:4  
  *replacement file was available*  

- sub-094:  
  - File:sub-094_ses-1_task-training_run-1_bold.nii.gz  		Volume:5  
  - File:sub-094_ses-1_task-training_run-2_bold.nii.gz  		Volume:5  
  - File:sub-094_ses-1_task-training_run-3_bold.nii.gz  		Volume:3  
  - File:sub-094_ses-1_task-training_run-4_bold.nii.gz  		Volume:2  
  *no replacement files available, will probably have to remove subject*  

- sub-128:  
  - File:sub-128_ses-1_task-training_run-1_bold.nii.gz  		Volume:154
  - File:sub-128_ses-1_task-training_run-2_bold.nii.gz  		Volume:131
  - File:sub-128_ses-1_task-training_run-3_bold.nii.gz  		Volume:131
  - File:sub-128_ses-1_task-training_run-4_bold.nii.gz  		Volume:147  
  *no replacement files available, will probably have to remove subject*  

- sub-146:  
  - File:sub-146_ses-1_task-training_run-1_bold.nii.gz  		Volume:76
  - File:sub-146_ses-2_task-training_run-4_bold.nii.gz  		Volume:19  
  *replacement file was available, subject has 3 runs*  

- sub-147:  
  - File:sub-147_ses-1_task-training_run-3_bold.nii.gz  		Volume:92  
  - File:sub-147_ses-1_task-training_run-4_bold.nii.gz  		Volume:123   
  *replacement run was available, subject now has 3 runs*

- sub-159:  
  - File:sub-159_ses-1_task-resting_bold.nii.gz  		Volume:68  
  *replacement file not available* 


## 2019-10  
### Added
- added dicom data onto RENCI at `bids/sourcedata/`
  * Session 1: 87 subjects  
  * Session 2: 66 subjects  
- bids formatted subjects added to `bids/` directory
  * Session 1: 87 subjects  
  * Session 2: 66 subjects  
