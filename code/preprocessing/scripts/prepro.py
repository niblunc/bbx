import glob, os, sys
import subprocess
import argparse
from multiprocessing import Pool
import functools
from datetime import date
import re


# -- Trim volumes Method with fslroi -- 

def trim_vols(func_file, outpath, overwrite=True, verbose=True):
    # strip off .nii.gz from file name (makes code below easier)
    func_file_no_nii = func_file.split(".")[0]
    func_filename = func_file_no_nii.split("/")[-1]
    
    
    # set out folder path
    if overwrite==False: 
        outfile= '%s/func/%s_trimmed'%(outpath,func_filename)
    else:
        outfile= '%s/func/%s'%(outpath,func_filename)
    
    #print(func_filename)
    # This is used to trim off unwanted volumes
    # DO NOT USE THIS UNLESS YOU'VE DOUBLE CHECKED HOW MANY
    # VOLUMES NEED TO BE TRIMMED (IF ANY)
    # This trims first 2 and I set the max to a number far beyond
    # the number of TRs
    # Correct filename here to use output of previous step (if used)
    tmin=4
    tsize=-1
    
    cmd=['fslroi', '%s'%func_file_no_nii, outfile, str(tmin), str(tsize)]
     # get volume to see if we want to trim it
    vol = subprocess.check_output(["fslnvols", func_file])
    vol=str(vol,'utf-8').strip("\n")

    # check if volume has been extracted or not
    # -- we do not want to trim multiple times -- 
    # if vol is 233 (full original vol) we want to trim
    if vol == '233': #this is for TRAINING task (vols difer)
    
        if verbose ==True:
            print('[INFO] running command: \n', ' '.join(cmd))
        
        try:
            subprocess.run(cmd)
        except Exception as e:
            print('[INFO] error: ', e.message)
    else:
        print("[INFO] passing, training file already trimmed")
        pass
       


    
# -- Skull Strip (Brain Extraction) Method with fsl bet --

def brainX(func_file, outpath, verbose=True, overwrite=False):
    
    # setup variables and the command
    filename = func_file.split('/')[-1].strip('.nii.gz')[0]
    outpath = os.path.join(outpath, 'func','%s'%filename)
    bet_cmd = ['bet' ,'%s'%func_file, outpath, '-F']
    
    
    # check if file exists and if it should be overwritten or not (default no)    
    if os.path.exists(outpath) and overwrite==False:
        print('\n[INFO] file already exists, %s'%outpath)
        pass
    
    # run bet command  
    else:
        if verbose == True:
            print('\n[INFO] running command: \n', ' '.join(bet_cmd))
        try:
            bet_process = subprocess.Popen(bet_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, errors = bet_process.communicate()

        except Exception as e:
            print('[INFO] error: ', e)
        
        
# -- Motion Correction Method with fsl_motion_outliers --        
def MOCO(func_file, outpath, moco_overwrite=False, verbose=True):
    
    # Set variables
    filename = func_file.split(".")[0]
    
    confound_filename = os.path.join(outpath, '%s_confounds.txt'%filename.split("/")[-1])
    plotpt_filename = os.path.join(outpath,'%s_moco.png'%filename.split("/")[-1])

    moco_cmd = ['fsl_motion_outliers', '-i', func_file, '-o', confound_filename, '-p', plotpt_filename, '--fd', '--thresh=0.9', '-v']
    
    
    outlier_txt = os.path.join(outpath, 'outliers_output.txt')
    
    print(confound_filename)
    
    #outhtml = "/projects/niblab/experiments/bbx/data/test/prepro_pipeline/bold_motion_QA.html"

    try:
        
        
        with open(outlier_txt, 'w') as txtf:
            # run fsl_motion_outiers command
            moco_process=subprocess.Popen(moco_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) 
            if verbose ==True:
                print('[INFO] running command: \n', ' '.join(moco_cmd))
            stdout, stderr = moco_process.communicate()
            moco_process.wait()
            txtf.write(stdout)
        txtf.close()
     
        
        confound_file=os.path.join(outpath, confound_filename)
        print("[INFO] confound file outpath: %s"%confound_file)
        if not os.path.exists(confound_file):
            touch_cmd=["touch", "%s"%(confound_file)]
            if verbose==True:
                print('[INFO] making empty confound file with command: ', ' '.join(touch_cmd))
            subprocess.run(touch_cmd)
        
        
        
        confound_output = subprocess.check_output("grep -o 1 %s | wc -l"%(confound_file), shell=True)
        
        num_scrub = [int(s) for s in confound_output.split() if s.isdigit()]
        
        vol = subprocess.check_output(["fslnvols", func_file])
        vol=str(vol,'utf-8').strip("\n")
        vol_check=int(vol)*.25
        
        out_bad_bold_list = os.path.join('/projects/niblab/experiments/bbx/data/quality_analysis/bbx_ses-1_vol_scrub.txt')
        if num_scrub[0]>vol_check:
            if verbose==True:
                print('[INFO] writing to scrub list')
            with open(out_bad_bold_list, "a") as myfile:
                myfile.write("%s\n"%(func_file))
            
    except Exception as e:
        print('[INFO] error: ', e)

        
    #print("[INFO] fsl_motion_outliers process complete")

        
        
# main() method
        
def main(arglist):
    
    print("\n[INFO] starting program....")
    
    # get data and set starting variables
    bet_data_path = arglist['BRAINX']
    trim_data_path = arglist['TRIM']
    moco_data_path = arglist['MOCO']
    outpath= arglist['OUTPATH']
    subject = arglist['SUB']
    ses = arglist['SES']
    
    # set outfolder for the session and subject
    outfolder=os.path.join(outpath, '%s/%s'%(subject, ses)) 
    today = date.today()
    
    
    
    # -- Case 1: Brain Extraction (bet) -- 
    if arglist['BRAINX'] != False:
        functionals=glob.glob(os.path.join(bet_data_path,
                                           subject, ses,'func/*.nii.gz'))
        #print('[INFO] %s'%functionals)
        
        pool = Pool()
        pool.map(functools.partial(brainX, outpath=outfolder), functionals)
        pool.close()
        
    # -- Case 2: Volume Trim (fslroi) -- 
    if arglist['TRIM'] != False:
        print('[INFO] data path: %s'%trim_data_path)
        # grab functionals 
        
        # here is a regex path that grabs all available functionals found in the file
        # adjust the regex here to grab specific files
        # currently it grabs all FMRIPREP training runs
        func_files_path=os.path.join(trim_data_path,subject, ses,'func/%s_%s_task-training_run-[1234]_space-MNI152NLin2009cAsym_desc-preproc_bold_brain.nii.gz'%(subject,ses))
        functionals=glob.glob(func_files_path)
        functionals.sort()
        print('[INFO] functionals found: %s'%len(functionals))
        
        # run parallel program 
        pool = Pool()
        pool.map(functools.partial(trim_vols, outpath=outfolder, overwrite=True), functionals)
        pool.close()

    
    # -- Case 3: Motion Correction (fsl_motion_outlier) --       
    if arglist['MOCO'] != False:
        motion_outpath=os.path.join(outfolder, "func/spike_confounds")
        if not os.path.exists(motion_outpath):
            os.makedirs(motion_outpath)
        print("[INFO] motion outliers output path: ", motion_outpath)
        
        #if not os.path.exists(motion_outpath):
         #   os.makedirs(motion_outpath)
        
        moco_funcs=glob.glob(os.path.join(moco_data_path,
          subject, ses, 'func', '%s_%s_task-training_run-[1234]_space-MNI152NLin2009cAsym_desc-preproc_bold_brain.nii.gz'%(subject,ses)))
        
        # run parallel program
        pool = Pool()
        pool.map(functools.partial(MOCO, outpath=motion_outpath), moco_funcs)
        #MOCO(functionals, subject, ses, basepath)
        pool.close()
               
            
            
# Setup for the optional user flags           
if __name__ == "__main__":
    
   # setup the commandline parser
    parser=argparse.ArgumentParser(description='Its for the streetz')
    
    parser.add_argument('-session', dest='SES', action='store',
                       default=False, help='which session are we running on?')
    
    parser.add_argument('-subject', dest='SUB', action='store', 
                        default=False, help='which subject to analyze')
    
    parser.add_argument('-brainX', dest='BRAINX', action='store', 
                        default=False, help='BET skull strip')
    
    parser.add_argument('-moco', dest='MOCO', action='store', 
                        default=False, help='fsl outliers motion correction, enter input data path where the subjects are found,  i.e "/projects/niblab/experiments/bbx/data')
    
    parser.add_argument('-trim', dest='TRIM', action='store', 
                        default=False, help='volume cutitng with fslroi, enter input data path where the subjects are found,  i.e "/projects/niblab/experiments/bbx/data')
    
    parser.add_argument('-overwrite_trim', dest='OVERWRITE_TRIM', action='store_true', 
                        default=False, help='overwrite trim files?')
    parser.add_argument('-extractpath', dest='BETPATH',
                        action='store', help='path where the data to be extracted can be found, i.e "/projects/niblab/experiments/bbx/data"')
    
    #parser.add_argument('-trimdata', dest='TRIMPATH',
                 #       action='store', help='path where the data to be trimmed can be found, i.e "/projects/niblab/experiments/bbx/data"')
    
    #parser.add_argument('-mocodata', dest='MOCOPATH',
                       # action='store', help='path where the data to run fsl motion outliers can be found (by subject folders), i.e "/projects/niblab/experiments/bbx/data"')
    
    parser.add_argument('-outpath', dest='OUTPATH',
                        action='store', help='output path')
    
    
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        
        
    # call main() with the parser list
    main(arglist)
    
    