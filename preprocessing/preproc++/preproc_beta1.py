#!/usr/bin/env
# -*- coding: utf-8 -*-



import argparse
import glob
import pandas as pd
import argparse
import os
from multiprocessing import Pool
import subprocess
import datetime
from functools import partial

import shutil


def fd_check(args, ses_id, sub_list):
    datestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

    outhtml = os.path.join(args.BIDS, "derivatives", 'ses-%s_bold_motion_QA_%s.html' % (ses_id, datestamp))
    out_bad_bold_list = os.path.join(args.BIDS, "derivatives", 'ses-%s_TEST_%s.txt' % (ses_id, datestamp))
    outfile = open(outhtml, 'a')
    TITLE = """<p><font size=7> <b> Motion Correction Check</b></font><br>"""
    outfile.write("%s" % TITLE)

    for sub in sub_list:
        print(">>>>---> Starting motion correction on ", sub)
        if ses_id == None:
            output_func_path = os.path.join(args.BIDS, "derivatives/{}/ses-{}/func".format(sub, ses_id))
        else:
            output_func_path = os.path.join(args.BIDS, "derivatives/{}/ses-{}/func".format(sub, ses_id))
            motion_assessment_path = os.path.join(output_func_path, "motion_assessment")

        if not os.path.exists(os.path.join(args.BIDS, "derivatives/{}/ses-{}".format(sub, ses_id))):
            os.makedirs(os.path.join(args.BIDS, "derivatives/{}/ses-{}".format(sub, ses_id)))
        if not os.path.exists(output_func_path):
            os.makedirs(output_func_path)
        if not os.path.exists(motion_assessment_path):
            os.makedirs(motion_assessment_path)
        try:
        # iterate over nifti file
            for nifti in glob.glob(os.path.join(output_func_path, '*_brain.nii.gz')):
                filename=nifti.split('.')[0]
                file = filename.split("/")[-1]
                new_filename = file.split("_bold_")[0]#.split("_space")[0]
                outlier_path = "%s/%s_outlier_output.txt"%(motion_assessment_path, new_filename)
                plot_path = "%s/%s_fd_plot"%(motion_assessment_path, new_filename)
                confound_path = "%s/%s_confound.txt"%(motion_assessment_path, new_filename)
                print(new_filename)
                #need to get identifier for tasks and runs --rn for bevel, need to specify for versatility
                #   set comparison param
                nvols_cmd="fslnvols " + nifti
                volume = subprocess.check_output(nvols_cmd, shell=True, encoding="utf-8")
                volume = volume.strip()
                comparator = int(volume) *.25
                # ## RUN 'fsl_motion_outliers' TO RETRIEVE MOTION CORRECTION ANALYSIS
                # outlier_cmd = "fsl_motion_outliers -i %s  -o %s --fd --thresh=%s -p %s -v > %s"%(filename, confound_path, args.FD, plot_path, outlier_path)
                # print(">>-->  RUNNING FSL MOTION OUTLIERS ")
                # #print("COMMAND NVOLS: ", nvols_cmd)
                # print("OUTLIER CMD: ", outlier_cmd)
                #
                # if not os.path.exists(confound_path):
                #     os.system(outlier_cmd)
                #
                # with open(outlier_path, 'r') as f:
                #     lines = f.readlines()
                #     statsA = lines[1].strip("\n")  # maskmean
                #     statsB = lines[3].strip("\n")  # metric range
                #     statsC = lines[4].strip("\n")  # outliers found
                #     if int(statsC.split(" ")[1]) > 0:
                #         statsD = lines[6].strip("\n")  # spikes found
                #     else:
                #         statsD = "\n"
                # f.close()

                plotz = plot_path + ".png"
                FILEINFO = """<p><font size=6> <b>{CURR_FILENAME} </b></font><br>"""
                CURR_FILEINFO = FILEINFO.format(CURR_FILENAME=file)
                outfile.write(CURR_FILEINFO)
                INFO = """<p><font size=6>{A} <br><b>{B}<b><br>{C}<br><b>{D}</b><br><br>"""
                CURR_INFO = INFO.format(A=statsA, B=statsB, C=statsC, D=statsD)
                outfile.write(CURR_INFO)
                PLOT = """<IMG SRC=\"{PLOTPATH}\" WIDTH=100%><br><br>"""
                CURR_PLOT = PLOT.format(PLOTPATH=plotz)
                outfile.write(CURR_PLOT)
                print(">>>>----> ADDING PLOT TO HTML")
                ## ADD FILE FOR GOOD SUBJECT
                # --sometimes you have a great subject who didn't move
                if os.path.isfile(confound_path) == False:
                    os.system("touch %s" % confound_path)
                ## CHECK FOR BAD SUBJECTS: ABOVE OUR THRESHOLD
                # how many columns are there = how many 'bad' points
                check = subprocess.check_output("grep -o 1 %s | wc -l" % (confound_path), shell=True)
                num_scrub = [int(s) for s in check.split() if s.isdigit()]
                print("NUM SCRUB: ", str(num_scrub[0]), "\n")
                if num_scrub[0] > comparator:  # if the number in check is greater than num_scrub then we don't want it
                    with open(out_bad_bold_list, "a") as myfile:  # making a file that lists all the bad ones
                        myfile.write("%s/%s\n" % (derivatives_dir, file))
                        print("wrote bad file")
                    myfile.close()



        except FileNotFoundError:
            pass

def write_files(filename, moco_df, outputdir):
    # iterate through the motion correction data frame by columns, writing individual columns to individual files
    for col in moco_df.columns:
        file= "%s_%s.txt"%(filename, col)
        output_path=os.path.join(outputdir, file)
        print("Writing to file, ", output_path)
        moco_df[col].to_csv(output_path, header=False, index=False)

def get_motion_parameters(args, ses_id, sub_list):
    errors = []
    try:
        for sub in sub_list:
            print("--------------> GETTING MOCOS FOR SUBJECT: ", sub)


            outputdir = os.path.join(args.BIDS, 'derivatives/{}/ses-{}/func/motion_assessment/motion_parameters'.format(sub, ses_id))
            print(outputdir)

            if ses_id != None:
                func_der_dir = os.path.join(args.BIDS, 'derivatives/{}/ses-{}/func'.format(sub, ses_id))
                func_fmriprep_dir = os.path.join(args.BIDS, 'derivatives/fmriprep/{}/ses-{}/func'.format(sub, ses_id))
            else:
                pass
            if not os.path.exists(os.path.join(outputdir)):
                os.makedirs(os.path.join(outputdir))


            confounds = glob.glob(os.path.join(func_fmriprep_dir, "*-confounds_regressors.tsv"))

            for tsv in confounds:
                print("-------> GRABBING NEW FILE:")
                print("FILE: ", tsv)

                df = pd.read_csv(tsv, sep="\t")
                #trans_x, trans_y, trans_z, rot_x, rot_y, rot_z are the 6 rigid-body motion-correction parameters estimated by fMRIPrep
                moco_df=df[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
                # ids for older fmriprep versions
                #moco_df=df[['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']]

                moco_df.columns = ['moco0', 'moco1', 'moco2', 'moco3', 'moco4', 'moco5']
                print("DATAFRAME: \n ", moco_df.head())
                filename = tsv.split('/')[-1].split("_desc")[0]
                print("FILENAME:", filename)

                write_files(filename, moco_df, outputdir)

    except FileNotFoundError as not_found:
        print("********************FILE NOT FOUND: ", not_found.filename)
        if sub not in errors:
            errors.append(sub)
        #print("ERRORS ", errors)
        #print("ERRORS SORTED ", sorted(errors))
    errors = sorted(errors)
    for err in errors:
        #print("ERROR" + err)
        file = os.path.join(args.BIDS, 'derivatives/error_files_moco.txt')

        with open(file, 'a') as f:
            f.write("----------> FILE NOT FOUND FOR SUBJECT: " + err  + "\n")
        f.close()




def skull_strip(args, ses_id, sub_list):
    for sub in sub_list:
        #print(ses_id)
        #print(args)
        print(">>>>---> starting bet on ", sub )

        if ses_id == None:
            fmriprep_path = os.path.join(args.BIDS, "derivatives/fmriprep/{}".format(sub))
        else:
            fmriprep_path = os.path.join(args.BIDS, "derivatives/fmriprep/{}/ses-{}".format(sub,ses_id))
            output_func_path =  os.path.join(args.BIDS, "derivatives/{}/ses-{}/func".format(sub, ses_id))

        if not os.path.exists(os.path.join(args.BIDS, "derivatives/{}/ses-{}".format(sub, ses_id))):
            os.makedirs(os.path.join(args.BIDS, "derivatives/{}/ses-{}".format(sub, ses_id)))
            os.makedirs(output_func_path)

        try:

            for nifti in glob.glob(os.path.join(fmriprep_path, "func",  '*-preproc_bold.nii.gz*')):
            # make our variables
                print("NIFTI: ", nifti)
                print(output_func_path)
                filename = nifti.split("/")[-1].split(".")[0]
                bet_name=filename+'_brain'
                print(bet_name)
                # check if data exists already
                bet_output = os.path.join(output_func_path, bet_name)
                if os.path.exists(bet_output + '.nii'):
                    print(bet_output + ' exists, skipping \n')
                else:
                    print("Running bet on ", nifti)
                    bet_cmd=("bet %s %s -F -m -f %s"%(nifti, bet_output, args.BET))
                    print(">>>-----> BET COMMAND:", bet_cmd)
                    #os.system(bet_cmd)
        except FileNotFoundError:
            pass




def main():

    print(args)

    # case: multiple (longitudinal) vs. single sessions scenario


    # check if case is a single session ( not expecting ~/sub-XXX/ses-XX/ format ):
    if args.SES == False:
        pass
    # else multi sessions will be found
    else:
        # case: if user wants to run all specific or all available sessions
        # if no specific session given find all sessions available and run
        if args.SES_ID == False:
            pass
        # else specific session given
        else:
            # get subjects
            for ses_id in args.SES_ID:


                subject_dir = glob.glob(os.path.join(arglist["BIDS"], "sub-*", "ses-%s"%(ses_id)))
                subjects = [x.split("/")[-2] for x in subject_dir]
                subjects = sorted(subjects)


                half = int(len(subjects) / 2)
                B, C = subjects[:half], subjects[half:]
                #print(B,C)

                pool = Pool(processes=2)
                #pool.map(run_program, [B, C])

                if args.BET != False:
                    # set relevant paths
                    #session_path =
                    func = partial(skull_strip, args, ses_id)
                    pool.map(func, [B,C])
                    pool.close()
                    #pool.join()

                if args.FD != False:

                    fd_pool = Pool(processes=2)

                    fd_func = partial(fd_check, args, ses_id)
                    fd_pool.map(fd_func, [B,C])
                    fd_pool.close()

                if args.MOTION == True:
                    mot_pool = Pool(processes=2)
                    mot_func = partial(get_motion_parameters, args, ses_id)
                    mot_pool.map(mot_func, [B,C])

            """# run given flags:
            if args.DIR == True:
                check_output_directories(sub, derivatives_dir, anat_output_path, func_output_path)
            if args.ANAT != False:
                move_anat(sub, anat_fmri_path, anat_output_path)

            if args.MOTION == True:
                get_motion_parameters(sub, fmriprep_dir, motion_assessment_path, func_input_path)"""




# Start Program
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='preprocessing')
    #parser.add_argument('-task',dest='TASK', default=False, help='which task are we running on?')

    parser.add_argument('-fd',dest='FD',
                        default=False, help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS, pass in threshold variable, 0.9 is common')
    parser.add_argument('-bet',dest='BET',
                        default=False, help='bet via fsl using defaults for functional images, pass in strip variable for fractional intensity')
    parser.add_argument('-ses_id',dest='SES_ID', nargs="+",
                        default=False, help='have multiple sessions?')
    parser.add_argument('-ses', dest='SES', action="store_true",
                       default=False, help='have multiple sessions?')
    parser.add_argument('-motion',dest='MOTION', action="store_true",
                        default=False, help='output 1 column motion parameter text files')
    parser.add_argument('-bids',dest='BIDS',
                        default=False, help='enter path for bids/ directory')
    parser.add_argument('-anat',dest='ANAT', default=False, action='store_true',
                        help='add flag if you want to move the anatomical image into the derivatives folder from fmriprep')
    parser.add_argument('-makedir',dest='DIR', default=False, action='store_true',
                        help='add flag if you want to make the output directories')

    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

    main()
