#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
import os
import node
import init_calculation
import adsorption_calculation


args = sys.argv
file_url = args[1]
calculation_mode = args[2]
part = args[3]
homepath = os.path.expanduser('~')
print("Extracting Helium Void Fraction values")
work_dir = init_calculation.init_calc_space(file_url)
for mofpath in work_dir:
    essential_cif = init_calculation.seek_mof_cif(mofpath)
    os.chdir(mofpath)
    calc_cif = init_calculation.babel_cif("".join(essential_cif) + ".cif")
    init_calculation.init_mof_ppcalc(mofpath,calculation_mode,part)
mofs = [i for i in os.listdir(file_url) if not str(i).split(".")[-1] == "cif"]
#mofs = os.listdir(file_url)
for mof in mofs:
    filepath = file_url + os.sep + "".join(mof)
    try:
        shpath =  adsorption_calculation.apply_pressure(filepath,calculation_mode,part)
        print(shpath)
    except FileNotFoundError:
        print(mof,"  Helium void Fraction was not found")
        continue 
#submit job
print("creating the batch scripts...")
node.creat_workdir(homepath,calculation_mode,part)
#node.split_job(mode,shpath,part)
print("Start submitting mof "+ calculation_mode +" calculation work...")
submission = node.submit_job(calculation_mode,shpath,part)
if submission is True:
    os.chdir(file_url)
    print("now remove excess cif file...")
    os.system("rm *.cif")
    exit(0)
