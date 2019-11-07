import glob
import os
from subprocess import check_output
import argparse
import re


def make_file(sub,main_dict):

    if args.SESS == False and args.ALL_SESS == False: # or task == ('resting' || 'rest')
        # case - no sessions
        pass

    elif args.ALL_SESS == True:
        # case - grab all available sessions
        pass

    else:
        # case - grab only specified sessions

        # loop through sessions
        for sess_id in args.SESS:


            if arglist["RUN"] == False:
                # case - no runs, only task (i.e. resting)
                pass

            else:
                # case - session, runs available
                for run in main_dict[sub]:
                    #print(run)

                    with open(args.FSF_FILE, 'r') as infile:
                        print("Opening template file {}".format(args.FSF_FILE))
                        tempfsf = infile.read()

                        #  fill in tempfsf file with parameters
                        tempfsf = tempfsf.replace("OUTPUT", main_dict[sub][run]["OUTPUT"])
                        tempfsf = tempfsf.replace("FUNCRUN", main_dict[sub][run]["FUNC"])
                        tempfsf = tempfsf.replace("TR", main_dict[sub][run]['TR'])
                        tempfsf = tempfsf.replace("CONFOUND", main_dict[sub][run]['CONFOUND'])
                        tempfsf = tempfsf.replace("VOL", main_dict[sub][run]['VOL'])

                        # loop through keys in dict to find EVs and MOCOs
                        for key in main_dict[sub][run]:


                            # Fill in EVS
                            if re.match(r'EV', key):
                                ev_name = key.split("_")[1]
                                ev = main_dict[sub][run][key]
                                tempfsf = tempfsf.replace(ev_name, ev)
                                #print(ev_name, "\n", ev)

                            if re.match(r'MOCO', key):
                                print(key)
                        print(tempfsf)

    """for run in arglist["RUN"]:
        with open(args.FSF_FILE, 'r') as infile:
            tempfsf = infile.read()


            for key2 in main_dict[key][run]:
                if re.match(r'EV[0-9]TITLE', key2):
                    ev_title = main_dict[key][run][key2]
                    n = re.findall('\d+', key2)
                    n = ''.join(str(x) for x in n)
                    ev = main_dict[key][run]["EV%s" % n]
                    print("EVTITLE: ", ev_title)
                    print("EV%s" % n, ev)
                    # tempfsf = tempfsf.replace("EV%sTITLE"%n, ev_title)
                    tempfsf = tempfsf.replace("EV%s" % n, ev)

            for i in range(6):
                moco = main_dict[key][run]["MOCO%i" % i]
                tempfsf = tempfsf.replace("MOCO%i" % i, moco)
                print("MOCO%i: " % i, main_dict[key][run]["MOCO%i" % i])
            outpath = os.path.join(deriv_dir, key, 'func', 'Analysis', "feat1")
            # print(tempfsf)
            if not os.path.exists(outpath):
                os.makedirs(outpath)
            print("OUT PATH >>>>>>---------> ", outpath)
            with open(os.path.join(outpath, '%s_task-%s_run-%s_no_reg.fsf' % (key, arglist['TASK'], run)),
                      'w') as outfile:
                outfile.write(tempfsf)
            outfile.close()
        infile.close()"""


def fill_dict(sub, main_dict):
    task = arglist['TASK']
    deriv_path = args.DERIVDIR
    sub_path = os.path.join(deriv_path, sub)
    #print("SUBJECT: %s \t TASK: %s \nPATH: %s"% (sub, task, sub_path))

    if args.SESS == False and args.ALL_SESS == False: # or task == ('resting' || 'rest')
        # no sessions
        pass

    elif args.ALL_SESS == True:
        # grab all available sessions
        pass

    else:
        # only specified sessions
        for sess_id in args.SESS:

            if arglist["RUN"] == False:
                # case for no runs, only task (i.e. resting)
                pass
            else:
            # 2 cases: individual/given runs or all runs found

                # case 1: if flag false, grab all available runs found
                if arglist["RUNS"] == False:
                    funcs_found = glob.glob(os.path.join(deriv_path, sub, 'func',
                                                 "%s_ses-%s_task-%s_run-*preproc*brain.nii.gz" % (sub, sess_id, task)))
                    runs=[x.split("/")[-1].split("_")[3].split("-")[1] for x in funcs_found]
                    for run in runs:
                        main_dict[sub][run] = {}
                    print("Dictionary initialized as: {}".format(main_dict[sub]))

                    for func in funcs_found:
                        x = int(run)
                        run=func.split("/")[-1].split("_")[3].split("-")[1]
                        output_path=os.path.join(sub_path, 'func', 'Analysis', 'feat1', 'ses-%s_task-%s_run-%s' % (sess_id, task, run))
                        confound = os.path.join(deriv_path, sub, 'func', 'motion_assessment',
                                         '%s_ses-%s_task-%s_run-%s_space-MNI152NLin2009cAsym_desc-preproc_confound.txt' % (sub, sess_id, task, run))

                        # fill dictionary
                        main_dict[sub][run]['OUTPUT'] = output_path

                        scan = func.split(".")[0]
                        main_dict[sub][run]['FUNC'] = scan
                        vol = check_output(['fslnvols', scan])
                        vol = vol.decode('utf-8')
                        vol = vol.strip('\n')
                        main_dict[sub][run]['VOL'] = vol
                        main_dict[sub][run]['CONFOUND'] = confound

                        # -- TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
                        trs = check_output(['fslval', '%s' % (scan), 'pixdim4', scan])
                        trs = trs.decode('utf-8')
                        trs = trs.strip('\n')
                        # print("TRs: ", trs)
                        main_dict[sub][run]['TR'] = trs

                        for i in range(6):
                            motcor = os.path.join(sub_path, 'func', 'motion_assessment', 'motion_parameters',
                                              '%s_ses-%s_task-%s_run-%s_moco%s.txt' % (sub, sess_id, task, run, i))
                            main_dict[sub][run]['MOCO%i' % i] = motcor

                        # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

                        ctr = 0
                        for ev_name in arglist['EV']:
                            # print(item)
                            ctr = ctr + 1

                            ev = os.path.join(sub_path, 'func', 'onsets',
                                                  '%s_task-%s_run-%s.txt' % (sub, ev_name, run))
                            #print(ev)
                            # print("EV: ", ev)
                            main_dict[sub][run]['EV_%s' % ev_name] = ev





                    #print("TIMEPOINT: ", ntmpts)
                    #print("Dictionary initialized as: {}".format(main_dict[sub]))
                else:
                    ## go through runs given in arguments
                    pass



def main():
    #set_paths()
    # removed path function for now
    print("Starting program....")
    deriv_dir = args.DERIVDIR
    main_dict = {}
    ## case: Get all subjects available --add flag for individual subjects or passed list option
    for sub_path in sorted(glob.glob(os.path.join(deriv_dir, 'sub-*'))):
        sub = sub_path.split("/")[-1]
        print("Creating file for subject {}".format(sub))
        #set_dict(sub)
        main_dict[sub] = {}
        # set up dict for runs IF flag is passed

        fill_dict(sub, main_dict)
        #for x in main_dict[sub]["1"]:
            #print(x, main_dict[sub]["1"][x])
        make_file(sub, main_dict)

if __name__ == "__main__":

    # Setup the required/optional flags for user:
    parser = argparse.ArgumentParser(description='generates feat1 design.fsf files for indvidual subjects based on a template')
    parser.add_argument('-task', dest='TASK',
                        default=False, help='which functional task are we using?')
    parser.add_argument('-all_sess', dest='ALL_SESS', action='store_true',
                        default=False, help='grab and process all available sessions')
    parser.add_argument('-sess', dest='SESS',  nargs='+',
                        default=False, help='process specified session or sessions')
    parser.add_argument('-evs', dest='EV', nargs='+',
                        default=False, help='which evs are we using?')
    parser.add_argument('-all_runs', dest='RUN', action='store_true',
                        default=False, help='which run are we using?')
    parser.add_argument('-runs', dest='RUNS', nargs='+',
                        default=False, help='which run are we using?')
    parser.add_argument('-deriv_dir ', dest='DERIVDIR',
                        default=False, help='please enter your derivatives directory')
    parser.add_argument('-fsf ', dest='FSF_FILE',
                        default=False, help='please enter your FSF file path')
    args = parser.parse_args()
    arglist = {}
    for a in args._get_kwargs():
        arglist[a[0]] = a[1]
    main()


