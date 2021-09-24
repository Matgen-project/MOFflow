#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
import os
import node
import init_calculation
import adsorption_calculation

args = sys.argv
filepath = args[1]
mode = args[2]
part = args[3]
# prepare init_calculation
print("Creating the calculation directory...")
work_dir = init_calculation.init_calc_space(filepath)
for mofpath in work_dir:
    filename = init_calculation.seek_mof_cif(mofpath)
    os.chdir(mofpath)
    shpath = init_calculation.init_mof_ppcalc(mofpath,mode,part)
# submit init_calculation
homepath = os.path.expanduser('~')
print("creating the batch scripts...")
node.creat_workdir(homepath,mode,part)
node.split_job(mode,shpath,part)
print("Start submitting mof "+ mode + " calculation work...")
#yhbatch_id = node.submit_job(mode,shpath)
submission = node.submit_job(mode,shpath,part)
if submission is True:
    exit(0)
