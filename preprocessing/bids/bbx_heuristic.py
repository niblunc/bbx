# Nichollette Acosta

import os
#subject = os.environ["id"]

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anat/
    t1 = create_key('sub-{subject}/anat/sub-{subject}_{session}_T1w')


    # fmap/
    fmap_phase = create_key('sub-{subject}/fmap/sub-{subject}_{session}_phasediff')
    fmap_magnitude = create_key('sub-{subject}/fmap/sub-{subject}_{session}_magnitude')


    # func/
    rest = create_key('sub-{subject}/func/sub-{subject}_{session}_task-resting_bold')
    run = create_key('sub-{subject}/func/sub-{subject}_{session}_task-training_run-{item:01d}_bold')
    rl = create_key('sub-{subject}/func/sub-{subject}_{session}_task-rl_run-{item:01d}_bold')


    info = {t1: [],  fmap_phase: [], rest: [], run: [],  fmap_magnitude: [], rl: []}
    for s in seqinfo:
        print(s)
        if ('anat' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        try:
            if (s.dim3 == 36) and ('fmap' in s.protocol_name):
                info[fmap_phase].append(s.series_id)  ## append if multiple series meet criteria
            if (s.dim3 == 72) and ('fmap' in s.protocol_name):
                info[fmap_magnitude].append(s.series_id)  # append if multiple series meet criteria
        except:
            pass
        if  ('run' in s.protocol_name) and ('training' in s.protocol_name):
            info[run].append(s.series_id)  # append if multiple series meet criteria
        if ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria
        if  ('rl' in s.protocol_name):
            info[rl].append(s.series_id)


    return info
