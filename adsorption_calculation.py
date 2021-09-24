#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import init_calculation
import subprocess

''' 

Extract Helium void Fraction from before calculation and perform Adsorption calculation
: CIFPATH + INDIVIDUAL CIF DIRECTORY
eg: python MOFs_step2.py /WORK/nscc-gz_material_5/MOF/test/ref_try/mofdb/cif/ABAFUH.MOF_subset

'''

def read_outfile_name(single_mof_calcf):
    output_file_path = single_mof_calcf + "/HeliumVF/Output/System_0/"
    mof_id = single_mof_calcf.split("/")[-1]
    homepath = os.path.expanduser('~')
    print('the path is ', output_file_path)
    try:
        outfile_name = os.listdir(output_file_path)
        output_file = output_file_path+"".join(outfile_name)
        #print(output_file)
        #pat = "Rosenbluth factor new: (\d+.\d+)"
        pat = "Rosenbluth factor new: (\d+.\d+|\d+)"
        kw = 'Rosenbluth factor new'
        kwr = subprocess.getoutput("grep \'Rosenbluth factor new\' {}".format(output_file))
        #hvf_value = re.findall(pat,open(output_file).read())[-1]
        #hvf_value_list = re.findall(pat,open(output_file).read())
        print(kwr)
        hvf_value_list = re.findall(pat, kwr)
        print(hvf_value_list)
        if len(hvf_value_list) != 0:
            hvf_value = hvf_value_list[-1]
        else:
            hvf_value = None
    except FileNotFoundError:
        print(mof_id," no hvf value,skipping")  
        with open(homepath + "/MOFs/submit_state/adsorption_without_hvf.txt","a+") as f:
            f.writelines(mof_id)
        hvf_value = None

    return hvf_value

def modify_simulation_input(single_mof_calcf):
    hvf_value = read_outfile_name(single_mof_calcf)
    pat = "hvf_value"
    ads_path = single_mof_calcf + "/Adsorption"
    modify_file = ads_path + "/simulation.input"
    new_simulation = single_mof_calcf + "/Adsorption/newsimulation.input"
    open(new_simulation, 'w').write(re.sub(pat, str(hvf_value), open(modify_file).read()))
    os.system('mv '+ new_simulation + ' ' + modify_file)

    return ads_path

def apply_pressure(single_mof_calcf,mode,part):
    #pressure = ["5e7","1e4","5e4","1e5","5e5","1e6","1.5e6","2e7"]
    #N2
    #pressure = ["2e2", "4e4", "1e5"]
    #CH4	
    #pressure = ["5e4", "5e5", "100e5"]
    #CO2
    pressure = ["5e4"]
    #pressure = ["1e4", "5e5", "2e7"]
    #pressure = ["2e2","5e3","1e4","2e4","4e4","6e4","8e4","1e5"]
    diff_p_path = modify_simulation_input(single_mof_calcf)
    pat = "pressure_value"
    mol = "CO2"
    #mol = "methane"
    #mol = "N2"
    #print(diff_p_path)
    files = os.listdir(diff_p_path)
    #newin = "./new.input"
    #open("./simulation.input", 'w').write(re.sub("N2", mol, open(newin).read()))
    #os.system('mv new.input simulation.input')
    homepath = os.path.expanduser('~')
    adsorption_joblist_path = homepath + "/MOFs/work/MOF_Adsorption/"+ mode + "_" + part + os.sep
    for p in pressure:
        p_path = diff_p_path + os.sep + p + os.sep
        if not os.path.exists(p_path):
            os.mkdir(p_path)
        for i in files:
            ifile = diff_p_path + os.sep + i
            if os.path.isfile(ifile):
                shutil.copyfile(ifile, p_path + i)
        old_input_file = p_path + "/simulation.input"
        new_input_file = p_path + "/ap_simulation.input"
        new2_input_file = p_path + "CO2.input"
        cifname = init_calculation.seek_mof_cif(p_path)
        open(new_input_file, 'w').write(re.sub(pat, p, open(old_input_file).read()))
        open(new2_input_file, 'w').write(re.sub("N2", mol, open(new_input_file).read()))
        os.system('mv ' + new2_input_file + ' ' + old_input_file)
        os.remove(new_input_file)
        #homepath = os.path.expanduser('~')
        if not os.path.exists(adsorption_joblist_path):
            os.makedirs(adsorption_joblist_path)
        submit2_sh = ["#!/bin/sh\n",
                      "cd "+ p_path +"\n", 
                      "export RASPA_DIR=/WORK/nscc-gz_material_1/MOFs/sf_box/raspa2/src\n",
                      "#export RASPA_DIR=/WORK/nscc-gz_material_5/Apps/raspa2/src\n",
                      "$RASPA_DIR/bin/simulate\n"
                     ]
        os.chdir(adsorption_joblist_path)
        sub_file = "ads" + "".join(cifname) +"_"+ p + ".sh"
        with open(r"./" + sub_file, "w") as f_sub:
            f_sub.writelines(submit2_sh)

    return adsorption_joblist_path

if __name__ == '__main__':
    import sys
    args = sys.argv
    single_mof_calcf = args[1]
    mode = args[2]
    part = args[3]
    apply_pressure(single_mof_calcf,mode,part)
