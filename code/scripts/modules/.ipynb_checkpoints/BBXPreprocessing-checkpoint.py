# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:02:38 2021

@author: Nichollette Acosta
"""

"""
# import packages 
"""

import os, glob, shutil, sys
import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import subprocess as sp
import seaborn as sns
from nilearn import image, plotting
from multiprocessing import Pool
from IPython.display import SVG, display
from datetime import date
from matplotlib import rcParams
import warnings


#sys.path.append("/projects/niblab/jupyter_notebooks")
#import fMRIPreprocessing


plt.rcParams['axes.titlepad'] = 15
plt.rcParams["figure.figsize"] = (20,15)

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
warnings.filterwarnings("ignore")

#%matplotlib inline 

class BBXPreprocessing:
    
    def set_params():
        """
        # Global Variables
        """
        
        date = date.today()
        study_folder_path="/projects/niblab/experiments/bbx"
        data_folder_path= os.path.join(study_folder_path, "data")
        report_folder_path= os.path.join(study_folder_path, "data/quality_analysis")
        bids_data_path=os.path.join(study_folder_path, "data/bids")
        
        
        
        
        sub_ids=[x.split("/")[-1] for x in glob.glob(os.path.join(study_folder_path,"data/bids/sub-*"))]
        sessions=['ses-1', 'ses-2']
        s1_dcm_subject_list=[x.split("/")[-2] for x in 
                           glob.glob(os.path.join(study_folder_path, "data/sourcedata/by_subject/sub-*/ses-1"))]
        s2_dcm_subject_list=[x.split("/")[-2] for x in 
                           glob.glob(os.path.join(study_folder_path, "data/sourcedata/by_subject/sub-*/ses-2"))]
        
        
########################################################################################
# BIDS 
    
    def run_bids_batch(job_file, sub, sess, x,y,z, submit_job=False):
        """
        # BIDS Batch Method
        """
        #print('[INFO] batch file: %s'%job_file)
        #id_int=sub.split("-")[1].lstrip('0')
        #batch_cmd='sbatch --array={}-{}%{} {}'.format(x,y,z, job_file)
        #print('[INFO] batch command: {}'.format(batch_cmd))
        
        # submit batch job
        if submit_job==True: 
            print(' '.join(['sbatch', '--array={}-{}%{}'.format(x, y, z), job_file, '2']))
            sp.run(['sbatch', '--array={}-{}%{}'.format(x, y, z), job_file, '2'])
            print('[INFO] submitted bids job.')
            
            
    # ---------------------------------- 
    # QUALITY REPORTS 
    
    def anat_plot(plot_filename, anat_img):
        # get anat file and save plot
        anat_plot=plotting.plot_anat(anat_img, title="%s_%s"%(subject,session),
             display_mode='ortho', dim=-1, draw_cross=False,
            annotate=False, output_file=plot_filename)
    
    def plot_functionals(func_file):
        # Compute the voxel_wise mean of functional images across time.
        # Basically reducing the functional image from 4D to 3D
        mean_img = image.mean_img(func_file)
        filename=func_file.split("/")[-1].split(".")[0]
    
        plot_filename = os.path.join(report_folder_path,
                                       "%s_mean_img.png"%filename)            
                
        plot_img=plotting.plot_epi(mean_img, title=filename,
            display_mode='ortho', draw_cross=False,
            annotate=False, output_file=plot_filename)
              
                
    
    # ---------------------------------- 
    
    def build_bids_report(write_files=False):


        print('[INFO] bids data folder: %s'%bids_data_path)
        #excel_file=os.path.join(report_folder_path, "bbx_preprocessing_report.xlsx")
        sessions=['ses-1', 'ses-2']
        dataframes=[]
        #writer = pd.ExcelWriter(excel_file, engine = 'xlsxwriter')
        logfile=open('/projects/niblab/experiments/bbx/data/quality_analysis/bad_volumes.log', 'a+')
        # loop through sessions
        for session in sessions:
            #print("\n[INFO] %s"%session)

            data_dict={} #initialize data dictionary for session

            # loop through subject set by subject
            for i in range(1,171):
                subject="sub-%s"%f'{i:03}'
                bids_folder=os.path.join(bids_data_path, subject,
                                        session)


                if subject not in data_dict:
                    data_dict[subject] = {}


                #--
                # get anat file

                anat_imgs =glob.glob(os.path.join(bids_folder, "anat",
                       '%s_%s_T1w.nii.gz'%(subject, session)))

                #if os.path.exists(anat_img): 
                    #plot_filename=os.path.join(report_folder_path, "%s_%s_anat.png"%(subject,session))
                data_dict[subject]["anat_file_ct"]=len(anat_imgs)
                #anat_plot(plot_filename, anat_img) #plot image

                # get fmap files

                fmap_magn_imgs =glob.glob(os.path.join(bids_folder, "fmap",
                       '%s_%s_magnitude[0-9].nii.gz'%(subject, session)))

                data_dict[subject]["fmap_magnitude_file_ct"]=len(fmap_magn_imgs)

                fmap_phase_imgs =glob.glob(os.path.join(bids_folder, "fmap",
                       '%s_%s_phasediff.nii.gz'%(subject, session)))
                data_dict[subject]["fmap_phasediff_file_ct"]=len(fmap_phase_imgs)

                # get functional files and check their volume and plot images
                func_files=glob.glob(os.path.join(
                        bids_folder, "func/*.nii.gz" ))

                # --initialize variables --
                train_ct=0
                rest_ct=0
                if session == 'ses-2':
                    rl_ct=0
                for func_file in func_files:
                    task=func_file.split("/")[-1].split("_")[2]
                    vol = sp.check_output(["fslnvols", func_file])
                    vol=str(vol,'utf-8').strip("\n")

                    if "resting" in task:
                        rest_ct+=1
                        var_name="%s_vol"%task
                        data_dict[subject][var_name]=vol
                        if vol != '212':
                            logfile.write("bad volume for %s %s %")

                    elif "rl" in task:
                        rl_ct+=1
                        run=func_file.split("/")[-1].split("_")[3]
                        var_name="%s_%s_vol"%(task,run)
                        data_dict[subject][var_name]=vol

                    elif "training" in task:
                        train_ct+=1
                        run=func_file.split("/")[-1].split("_")[3]
                        var_name="%s_%s_vol"%(task,run)
                        data_dict[subject][var_name]=vol


                if session == 'ses-2':
                    data_dict[subject]["rl_file_ct"]=rl_ct
                data_dict[subject]["train_file_ct"]=train_ct
                data_dict[subject]["rest_file_ct"]=rest_ct

            dataframe=pd.DataFrame(data_dict).T
            #dataframe.to_excel(writer, sheet_name="%s_bids"%session, index=False, header=False)
            dataframes.append(dataframe)
        print('[INFO] report building complete.')
        return dataframes;




########################################################################################


    
    """
    # Build FMRIPREP Report 
    
    """
    
    
    def build_fmriprep_report(write_files=False):
        
    
        sessions=['ses-1'] #, 'ses-2']
        dataframes=[]
            
        # loop through sessions
        for session in sessions:
            #print("\n[INFO] %s"%session)
            
    
            data_dict={} #initialize data dictionary for session
    
            # loop through subject set by subject
            for i in range(1,171):
                train_ct=0
                rest_ct=0
                if session == 'ses-2':
                    rl_ct=0
                subject="sub-%s"%f'{i:03}'
                bids_folder=os.path.join(fmriprep_path, subject,
                                        session)
    
                if subject not in data_dict:
                    data_dict[subject] = {}
    
    
    
                # get anat file and save plot
                #_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.g
                anat_img =os.path.join(fmriprep_path, subject, "anat",
                       '%s_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz'%(subject))
    
                if os.path.exists(anat_img): 
                    data_dict[subject]["anat"]="good"
    
                # get functional files and check their volume and plot images
                func_files=glob.glob(os.path.join(
                        fmriprep_path, subject, session,
                        "func/*task-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz" ))
    
                for func_file in func_files:
                    
                    task=func_file.split("/")[-1].split("_")[2]
                    vol = sp.check_output(["fslnvols", func_file])
                    vol=str(vol,'utf-8').strip("\n")
    
    
                    if "resting" in task:
                        rest_ct+=1
                        var_name="%s_vol"%task
                        data_dict[subject][var_name]=vol
                    elif "rl" in task:
                        rl_ct+=1
                        run=func_file.split("/")[-1].split("_")[3]
                        var_name="%s_%s_vol"%(task,run)
                        data_dict[subject][var_name]=vol
                    elif "training" in task:
                        train_ct+=1
                        run=func_file.split("/")[-1].split("_")[3]
                        var_name="%s_%s_vol"%(task,run)
                        data_dict[subject][var_name]=vol
    
                if session == 'ses-2':
                    data_dict[subject]["rl_file_ct"]=rl_ct
                data_dict[subject]["train_file_ct"]=train_ct
                data_dict[subject]["rest_file_ct"]=rest_ct
                # plot functionals
                #pool = Pool()
                #pool.map(plot_functionals, func_files)
                #pool.close()
    
            dataframe=pd.DataFrame(data_dict).T        
            dataframes.append(dataframe)
            #dataframe.to_excel(writer, sheet_name="%s_fmriprep"%session)
        #writer.save()
        #writer.close()
        return dataframes;
    
    
    def bbx_feat1():

        preproc_dir = "/projects/niblab/experiments/bbx/data/preprocessed"
        main_dict = {}
        fsf_template = os.path.join('/projects/niblab/experiments/bbx/data/preprocessed/fsl_feat1.fsf')
        onset_path='/projects/niblab/experiments/bbx/data/onsets/trimmed_evs'
    
        print('[FSL TEMPLATE] %s'%fsf_template)
    
        for sub in sub_ids:
    
            task = "training"
            sessions = ["ses-1"]#, "ses-2"]
            evs = ['SSBtaste', 'USBtaste', 'H2Otaste', 'H2Ocue', 'SSBcue', 'USBcue', 'rinse']
    
            all_runs = True
    
            #print("SUBJECT: %s \t TASK: %s \nPATH: %s"% (sub, task, sub_path))
    
    
            for sess_id in sessions:
                sess_path=os.path.join(study_path, 'data/preprocessed/subs_trimmed/%s/%s'%(sub, sess_id))
                #print(sess_path)
                if task == 'resting':
                    # case for no runs, only task (i.e. resting)
                    pass
                else:
                # 2 cases: individual/given runs or all runs found
    
                    # case 1: if flag false, grab all available runs found
                    if all_runs == True:
                        #sub-001_ses-2_task-resting_space-MNI152NLin2009cAsym_desc-preproc_bold_brain.nii.gz
                        funcs_found = glob.glob(os.path.join(study_path, 'data/preprocessed/subs_trimmed/%s/%s/func'%(sub, sess_id),
                                                     "%s_%s_task-%s_run-*preproc_bold_brain.nii.gz" % (sub, sess_id, task)))
                        runs=[x.split("/")[-1].split("_")[3].split("-")[1] for x in funcs_found]
    
                        for func in funcs_found:
                            run=func.split("/")[-1].split("_")[3].split("-")[1]
                            x = int(run)
    
                            # SET OUTPUT PATH FOR FEAT DIRECTOR
                            output_path=os.path.join(study_path, 'data/preprocessed/subs_trimmed/%s/%s'%(sub, sess_id),
                                                     'fsl_feat1', '%s_%s_task-%s_run-%s'%(sub, sess_id,task, run))
    
                            #print("[OUTPUT PATH] ", output_path)
    
    
                            # SET CONFOUND
                            # sub-004_ses-1_task-resting_space-MNI152NLin2009cAsym_desc-preproc_confound.txt
                            # %s_ses-%s_task-%s_run-%s_confound.txt
                            confound = os.path.join(preproc_dir, 'confounds_trimmed', "fmriprep_fd_spikes",
                                                    '%s_%s_task-%s_run-%s_fd_spikes.txt'%(sub,sess_id, task, run))
    
                            scan = func.split(".")[0]
                            # TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
                            trs = sp.check_output(['fslval', '%s' % (scan), 'pixdim4', scan])
                            trs = trs.decode('utf-8')
                            trs = trs.strip('\n')
    
                            vol = sp.check_output(['fslnvols', scan])
                            vol = vol.decode('utf-8')
                            vol = vol.strip('\n')
    
                            with open(fsf_template, 'r') as infile:
                                tempfsf = infile.read()
    
                                #  fill in tempfsf file with parameters
                                tempfsf = tempfsf.replace("OUTDIR",output_path)
                                tempfsf = tempfsf.replace("FUNCTIONAL",scan)
                                tempfsf = tempfsf.replace("TR", trs)
                                tempfsf = tempfsf.replace("CONFOUND", confound)
                                tempfsf = tempfsf.replace("VOL",vol)
    
    
                                # SET MOTION PARAMETERS
                                for i in range(6):
                                    motcor = os.path.join(preproc_dir, 'confounds_trimmed', 'basic_head_confounds',
                                                          '%s_%s_task-%s_run-%s_moco%s.tsv' % (sub, sess_id, task, run, i))
                                    #main_dict[sub][run]['moco%i' % i] = motcor
                                    moco_name=motcor.split("/")[-1].split(".")[0].split("_")[4]
                                    tempfsf = tempfsf.replace(moco_name+"_file", motcor)
                                    
                                    
                                    acompcor=os.path.join(preproc_dir, 'confounds_trimmed', 'acompcor',
                                                  '%s_%s_task-%s_run-%s_a_comp_cor_0%s.tsv' % (sub, sess_id, task, run, i))
                                    tempfsf = tempfsf.replace("acompcor%s_file"%i, motcor)
                                    
                                    
                                
    
                    
                                # SET EVS
                                # Loop through the given EVs and add the corresponding file to the dictionary
    
                                ctr = 0
                                for ev_name in evs:
                                    # print(item)
                                    ctr = ctr + 1
    
                                    ev = os.path.join(onset_path, '%s_%s_task-%s_run-%s_trimmed.txt' % (sub,sess_id, ev_name, run))
                                    #if ev_name == "H2O":
                                     #   ev_name = "h2Otaste"
                                    #if ev_name == "H2Ocue":
                                     #   ev_name = "h2Ocue"
    
                                    #print(ev_name)
                                    #print('[EV%s] %s'%(ctr,ev))
                                    #print('[EV NAME] 'ev_name)
                                    tempfsf = tempfsf.replace(ev_name+"_file", ev)
    
    
                                fsf_outfile = '%s_%s_task-%s_run-%s.fsf'%(sub, sess_id,task, run)#, today)
                                fsf_outpath = os.path.join(study_path, 
                                                           "data/preprocessed/subs_trimmed/%s/%s/fsl_feat1"%(sub, sess_id),
                                                           fsf_outfile)
                                #print("[FSF OUTFILE] ",fsf_outpath)
                                with open(fsf_outpath, 'w') as outfile: #os.path.join(outpath,
                                    outfile.write(tempfsf)
                                outfile.close()
                            infile.close()
            print('[INFO] writing process complete for fsl feat1 fsf files.')
    
