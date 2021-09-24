#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import MOFs_step1

''' 

Extract Helium void Fraction from before calculation and perform Adsorption calculation
: CIFPATH + INDIVIDUAL CIF DIRECTORY
eg: python MOFs_step2.py /WORK/nscc-gz_material_5/MOF/test/ref_try/mofdb/cif

'''

def find_path(calc_dir):
    filepath_list = os.listdir(calc_dir) 
    
    return filepath_list
def read_output(filepath):
    global wrong_calc_filepath
    homepath = os.path.expanduser('~')
    wrong_calc_filepath = homepath + "/MOFs/wrong_hc_calc/" 
    if not os.path.exists(wrong_calc_filepath):
        os.makedirs(wrong_calc_filepath)
    output_file_path = filepath +"/HeliumVF/Output/System_0/"
    try:
        ofn = os.listdir(output_file_path)
        output_file = output_file_path+"".join(ofn)
        check_result = check_calc_if_finished(output_file)
        if check_result is not True:
            cifname = filepath.split("/")[-1] + ".cif"
            shutil.copyfile(filepath + "/" + cifname ,wrong_calc_filepath + cifname)
            hc_value = None
        else:
            #pat = "Rosenbluth factor new: (\d+.\d+)"
            pat = " Average Henry coefficient:  (.*?) [+]"
            try:
                hc_value = re.findall(pat,open(output_file).read())[-1]
            except:
                print("The outputfile has no henryc value")
                if not os.path.exists(wrong_calc_filepath):
                    os.makedirs(wrong_calc_filepath)
                cifname = filepath.split("/")[-1] + ".cif"
                srcfile = filepath + "/" + cifname
                desfile = wrong_calc_filepath + cifname
                shutil.copyfile(srcfile ,desfile)
                hc_value = None
    except FileNotFoundError:
        #homepath = os.path.expanduser('~')
        print("failed to find outputfile,moving cif file..")
        cifname = filepath.split("/")[-1] + ".cif"
        srcfile = filepath + "/" + cifname
        #print(srcfile)
        desfile = wrong_calc_filepath + cifname
        #print(desfile)
        shutil.copyfile(srcfile ,desfile)
        hc_value = None

    return hc_value
'''
def filter_wrongcalc_cif(filename):
    homepath = os.path.expanduser('~')
    wrong_calc_filepath = homepath + "/MOFs/Wrong_calc/" 
    output_file_path = filepath +"/HeliumVF/Output/System_0/"
    try:
        ofn = os.listdir(output_file_path)
        output_file = output_file_path+"".join(ofn)
    except: 
        if not os.path.exists(wrong_calc_filepath):
            os.makedirs(wrong_calc_filepath)
        if not os.path.exists(output_file):
            cifname = filename.split("/")[-1] + ".cif"
            srcfile = filename + "/" + cifname
            print(srcfile)
            desfile = wrong_calc_filepath + cifname
            print(desfile)
            shutil.copyfile(srcfile ,desfile) 
 
    #if check_calc_if_finished(filename) is not True:
    #    shutil.copyfile(filename,wrong_calc_filepath+filename.split("/")[-1]) 
'''
def check_calc_if_finished(filename):
    check_pat_start = re.compile("Starting simulation")
    check_pat_end = re.compile("Simulation finished")
    with open(filename,"r") as f_check:
        data = f_check.read()
    #print(data)
    check_result = False
    mofname = str(filename.split("/")[-1])
    if check_pat_start.findall(data):
        print(mofname + " was submission sucessful")
    if check_pat_end.findall(data):
        print(mofname + " was calculated")
        check_result = True
    if check_result is not True:
        print(mofname + " calculation was not finished")
        with open("./unfinished_mof_job","a+") as f_check:
            f_check.writelines(mofname + "\n" + filename + "\n" )
    return check_result

def modify_input(filepath):
    hc_value = read_output(filepath)
    pat = "hc_value"
    ads_path = filepath + "/Adsorption"
    modify_file = ads_path + "/simulation.input"
    new_simulation = filepath + "/Adsorption/newsimulation.input"
    open(new_simulation, 'w').write(re.sub(pat, str(hc_value), open(modify_file).read()))
    os.system('mv '+ new_simulation + ' ' + modify_file)

    return ads_path

def apply_pressure(filepath):
    pressure = ["2e2","5e3","1e4","2e4","4e4","6e4","8e4","1e5"]
    diff_p_path = modify_input(filepath)
    pat = "pressure_value"
    #print(diff_p_path)
    files = os.listdir(diff_p_path)
    homepath = os.path.expanduser('~')
    adsorption_joblist_path = homepath + "/MOF_WORK/Joblist/Adsorption/"
    for p in pressure:
        p_path = diff_p_path + "/" + p + "/"
        os.mkdir(p_path)
        for i in files:
            shutil.copyfile(diff_p_path + "/" + i, p_path + i)
        old_input_file = p_path + "/simulation.input"
        new_input_file = p_path + "/ap_simulation.input"
        cifname = MOFs_step1.find_cif(p_path)
#P
        open(new_input_file, 'w').write(re.sub(pat, p, open(old_input_file).read()))
        os.system('mv ' + new_input_file + ' ' + old_input_file)
        #homepath = os.path.expanduser('~')
        #adsorption_joblist_path = homepath + "/MOF_WORK/Joblist/Adsorption/"
        if not os.path.exists(adsorption_joblist_path):
            os.makedirs(adsorption_joblist_path)
        submit2_sh = ["#!/bin/sh\n",
                      "cd "+ p_path +"\n", 
                      "export RASPA_DIR=/WORK/nscc-gz_material_5/Apps/raspa2/src\n",
                      "$RASPA_DIR/bin/simulate\n"
                     ]
        os.chdir(adsorption_joblist_path)
        sub_file = "ads" + str(cifname) +"_"+ p + ".sh"
        with open(r"./" + sub_file, "w") as f_sub:
            f_sub.writelines(submit2_sh)

    return adsorption_joblist_path

if __name__ == '__main__':
    import sys
    args = sys.argv
    filepath = args[1]
    workpath_list = find_path(filepath)
    for mof_name in workpath_list:
        mof_dir = filepath + "/" + mof_name
        print(mof_dir)
        hc_value = read_output(mof_dir) 
        if hc_value is not None:
            print("Writing calculation results....  " + mof_name )
            with open("./henry_coefficient_result.txt","a+") as f1:
                f1.writelines(str(mof_name) +" "*3 + format(str(hc_value),">s")+ "\n")
        else:
            with open("./wrong_result.txt","a+") as f2:
                f2.writelines(mof_name + "\n")
            continue
        #apply_pressure(pressure_path)
