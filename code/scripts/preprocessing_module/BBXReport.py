# -*- coding: utf-8 -*-

"""
BBX fMRI Scan Data Summary
@Organization: NIBL, UNC Chapel Hill
@Author: Nichollette Acosta
"""

# -- Packages --
import os, glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# -- Display Settings -- 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
plt.rcParams["figure.figsize"] = (15,12)


class BBXReport:
    c = 'class attribute'
    """This is AClass.c's docstring."""

    def __init__(self):
        """Method __init__'s docstring."""

        self.i = 'instance attribute'
        """This is self.i's docstring."""
        
    def bbx_summary(self):
        return None;
    def bbx_dcm_report(self, list_subs=False):
        print("\n**** BBX DICOM fMRI Scan Data ****\n")
        print("\n[INFO] 152 session 1 dicoms. (uploaded to renci)")
        if list_subs == True: print("SESSION-1 DICOMS: ['sub-001', 'sub-002', 'sub-003', 'sub-004', 'sub-005', 'sub-006', 'sub-007', 'sub-008', 'sub-009', 'sub-010', 'sub-011', 'sub-012', 'sub-013', 'sub-014', 'sub-015', 'sub-016', 'sub-017', 'sub-018', 'sub-019', 'sub-020', 'sub-021', 'sub-022', 'sub-023', 'sub-024', 'sub-025', 'sub-026', 'sub-027', 'sub-028', 'sub-030', 'sub-031', 'sub-032', 'sub-033', 'sub-034', 'sub-035', 'sub-036', 'sub-037', 'sub-038', 'sub-039', 'sub-040', 'sub-041', 'sub-042', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 'sub-051', 'sub-052', 'sub-053', 'sub-054', 'sub-055', 'sub-056', 'sub-057', 'sub-058', 'sub-059', 'sub-060', 'sub-061', 'sub-062', 'sub-063', 'sub-064', 'sub-065', 'sub-066', 'sub-067', 'sub-068', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 'sub-074', 'sub-075', 'sub-076', 'sub-077', 'sub-078', 'sub-079', 'sub-080', 'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-086', 'sub-087', 'sub-088', 'sub-089', 'sub-090', 'sub-091', 'sub-092', 'sub-093', 'sub-094', 'sub-095', 'sub-096', 'sub-097', 'sub-098', 'sub-099', 'sub-100', 'sub-102', 'sub-103', 'sub-104', 'sub-107', 'sub-108', 'sub-109', 'sub-111', 'sub-112', 'sub-114', 'sub-115', 'sub-116', 'sub-117', 'sub-118', 'sub-119', 'sub-120', 'sub-121', 'sub-123', 'sub-124', 'sub-127', 'sub-128', 'sub-129', 'sub-130', 'sub-131', 'sub-132', 'sub-133', 'sub-134', 'sub-135', 'sub-136', 'sub-137', 'sub-138', 'sub-140', 'sub-141', 'sub-142', 'sub-143', 'sub-144', 'sub-145', 'sub-146', 'sub-147', 'sub-148', 'sub-149', 'sub-150', 'sub-151', 'sub-152', 'sub-153', 'sub-154', 'sub-156', 'sub-157', 'sub-159', 'sub-160', 'sub-162', 'sub-163', 'sub-164', 'sub-166', 'sub-167', 'sub-168', 'sub-169', 'sub-170']")


        print("\n[INFO] 140 session 2 dicoms. (uploaded to renci)")
        if list_subs == True: print("SESSION-2 DICOMS: ['sub-001', 'sub-002', 'sub-004', 'sub-005', 'sub-006', 'sub-007', 'sub-008', 'sub-009', 'sub-010', 'sub-011', 'sub-013', 'sub-014', 'sub-015', 'sub-016', 'sub-017', 'sub-019', 'sub-020', 'sub-021', 'sub-022', 'sub-023', 'sub-024', 'sub-025', 'sub-027', 'sub-028', 'sub-030', 'sub-031', 'sub-032', 'sub-033', 'sub-034', 'sub-035', 'sub-036', 'sub-037', 'sub-038', 'sub-039', 'sub-040', 'sub-041', 'sub-042', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 'sub-051', 'sub-052', 'sub-053', 'sub-054', 'sub-055', 'sub-057', 'sub-058', 'sub-059', 'sub-061', 'sub-062', 'sub-063', 'sub-065', 'sub-066', 'sub-067', 'sub-068', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 'sub-074', 'sub-075', 'sub-077', 'sub-078', 'sub-079', 'sub-080', 'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-086', 'sub-087', 'sub-088', 'sub-089', 'sub-090', 'sub-092', 'sub-093', 'sub-094', 'sub-095', 'sub-096', 'sub-097', 'sub-098', 'sub-099', 'sub-100', 'sub-102', 'sub-103', 'sub-104', 'sub-107', 'sub-108', 'sub-109', 'sub-111', 'sub-112', 'sub-114', 'sub-115', 'sub-116', 'sub-117', 'sub-118', 'sub-119', 'sub-120', 'sub-121', 'sub-123', 'sub-124', 'sub-127', 'sub-128', 'sub-129', 'sub-130', 'sub-131', 'sub-132', 'sub-133', 'sub-134', 'sub-136', 'sub-137', 'sub-140', 'sub-141', 'sub-142', 'sub-143', 'sub-144', 'sub-145', 'sub-146', 'sub-147', 'sub-148', 'sub-149', 'sub-151', 'sub-152', 'sub-153', 'sub-154', 'sub-156', 'sub-157', 'sub-159', 'sub-160', 'sub-161', 'sub-162', 'sub-163', 'sub-164', 'sub-166', 'sub-168', 'sub-169', 'sub-170']")

    def bids_report(self):
        
        # load data
        bids_excel_path='../../data/xlsx/bbx_bids_report.xlsx'
        bids_s1_df=pd.read_excel(bids_excel_path, sheet_name="ses-1" )
        bids_s1_df = bids_s1_df.rename({'Unnamed: 0': 'patID'}, axis=1)
        bids_s2_df=pd.read_excel(bids_excel_path, sheet_name="ses-2" )
        bids_s2_df = bids_s2_df.rename({'Unnamed: 0': 'patID'}, axis=1)
        
        #print("\n[INFO] %s BIDS subject folders found for SESSION-1."%(len(bids_s1_df['patID'].values)))
        #print("\n[INFO] %s BIDS subject folders found for SESSION-2."%(len(bids_s2_df['patID'].values)))
        #display(bids_s1_df)
        print("\n**** BBX BIDS fMRI Scan Data ****\n")
        subject_ct_s1=len(bids_s1_df.loc[bids_s1_df['train_file_ct'] >= 2])
        print("\n[INFO] (SESSION-1) %s BIDS subject folders found.\n"%(subject_ct_s1))
        print('\n[INFO] (SESSION-1) %s subjects with 4 task-training run files.\n'%(len(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 4])))
        print('\n[INFO] (SESSION-1) %s subjects with 3 task-training run files.\n'%(len(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 3])))
        print('\n[INFO] (SESSION-1) %s subjects with 2 task-training run files.\n'%(len(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 2])))
        
        subject_ct_s2=len(bids_s2_df.loc[bids_s2_df['train_file_ct'] >= 2])
        print("\n[INFO] (SESSION-2) %s BIDS subject folders found.\n"%(subject_ct_s2))
        print("\n[INFO] (SESSION-2) %s subjects have 4 task-training run files."%(len(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 4])))
        print("\n[INFO] (SESSION-2) %s subjects have 3 task-training run files."%(len(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 3])))
        print("\n[INFO] (SESSION-2) %s subjects have 2 task-training run files."%(len(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 2])))
        print("----")
        
        # -- list subjects by runs available --
        print('\n(SESSION-1) SUBJECTS WITH 4 RUNS %s: \n'%(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 4]['patID'].values ))
        print('\n(SESSION-2) SUBJECTS WITH 4 RUNS %s:\n'%(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 4]['patID'].values ))
        print('\n(SESSION-1) SUBJECTS WITH 3 RUNS %s: \n'%(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 3]['patID'].values ))
        print('\n(SESSION-2) SUBJECTS WITH 3 RUNS %s:\n'%(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 3]['patID'].values ))
        print('\n(SESSION-1) SUBJECTS WITH 2 RUNS %s: \n'%(bids_s1_df.loc[bids_s1_df['train_file_ct'] == 2]['patID'].values ))
        print('\n(SESSION-2) SUBJECTS WITH 2 RUNS %s:\n'%(bids_s2_df.loc[bids_s2_df['train_file_ct'] == 2]['patID'].values ))
        print('---- \n')


        
    def display_imgs():
        img = mpimg.imread('../../data/pngs/sub-001_ses-1_anat.png')
        imgplot = plt.imshow(img)
        plt.show()


    
    