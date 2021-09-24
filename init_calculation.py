#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import math
import shutil
import readcif

''' 
Create an initial calculation folder and all simulation input file templates
(Helium void Fraction; Adsorption; Henry coefficient;) and calculate the unitcell value;
CIFPATH 
eg: python init_calculation.py ~/MOFs/cif
'''

def seek_mof_cif(file_url):
    f_list = os.listdir(file_url)
    cifs = [os.path.splitext(i)[0] for i in f_list if os.path.splitext(i)[1] == '.cif']

    return cifs

def init_calc_space(file_url):
    cifs = seek_mof_cif(file_url)
    init_calc_space_list = []
    essential_thing_extension = '.cif'
    for essential_thing in cifs:
        src_file = file_url + os.sep + essential_thing + essential_thing_extension
        des_path = file_url + os.sep + essential_thing + os.sep
        des_file = des_path + essential_thing + essential_thing_extension
        if not os.path.exists(des_path):
            os.mkdir(des_path)
        shutil.copy(src_file,des_file)
        init_calc_space_list.append(des_path)

    return init_calc_space_list

def babel_cif(essential_cif):
    mof_file = essential_cif
    calc_cif = mof_file
    #babel_mof_file = "babel_" + mof_file
    #babelcmd = "babel " + mof_file + " " + babel_mof_file
    '''
    try:
        os.system(babelcmd)
        os.remove(essential_cif)
        calc_cif = babel_mof_file
    except:
        print("babel conversion error!")
        calc_cif = mof_file
        with open("~/MOFslog","a+") as bb_error:
            bb_error.writelines(essential_cif+"\n")
    '''
    return calc_cif

def simulation_cell_value(essential_cif):
    cif_data = readcif.read_cif_file(essential_cif)
    lattice = readcif.get_lattice(cif_data)
    a, b, c = lattice[0], lattice[1], lattice[2]
    av, bv, cv = 0, 0, 0
    for i in range(3):
        av += a[i] ** 2
        bv += b[i] ** 2
        cv += c[i] ** 2
    av, bv, cv = math.sqrt(av), math.sqrt(bv), math.sqrt(cv)
    # print(av,bv,cv)
    #ra, rb, rc = 26 / av, 26 / bv, 26 / cv
    ra, rb, rc = 20 / av, 20 / bv, 20 / cv
    l = [ra, rb, rc]
    # print(l)
    #for num in range(3):
    #    if abs(l[num] - round(l[num])) < 0.5:
    #        l[num] += 1
    #    la, lb, lc = int(l[0]), int(l[1]), int(l[2])
    def _floor(x):
        a = math.floor(x)
        if a == 0:
            a = 1
        return int(x)
    la, lb, lc = list(map(_floor, l))
    if la == 0:
        la = 1
    if lb == 0:
        lb = 1
    if lc == 0:
        lc = 1
    
    length = str(la) + " " + str(lb) + " " + str(lc)

    return length

def init_mof_ppcalc(file_url,calculation_mode,section):
    homepath = os.path.expanduser('~')
    os.chdir(file_url)
    ppcalc_dir_list = ["HeliumVF","Adsorption","HenryC"]
    if calculation_mode == "hvf":
        joblist_path = homepath + "/MOFs/work/MOF_VoidFraction/"+ calculation_mode + "_" + section + os.sep
        if not os.path.exists(joblist_path):
            os.makedirs(joblist_path)
        ppath = ppcalc_dir_list[0]
    elif calculation_mode == "ads":
        joblist_path = homepath + "/MOFs/work/MOF_Adsorption/"+ calculation_mode + "_" + section + os.sep
        if not os.path.exists(joblist_path):
            os.makedirs(joblist_path)
        ppath = ppcalc_dir_list[1]
    elif calculation_mode == "hc":
        joblist_path = homepath + "/MOFs/work/MOF_HenryC/"+ calculation_mode + "_" + section + os.sep
        if not os.path.exists(joblist_path):
            os.makedirs(joblist_path)
        ppath = ppcalc_dir_list[2]
    else:
        raise NotSupport
    init_ppath = file_url + os.sep + ppath
    if not os.path.exists(init_ppath):
        os.makedirs(init_ppath)
    essential_cif = "".join(seek_mof_cif(file_url))
    essential_cif_extension = '.cif'
    cif_file = essential_cif + essential_cif_extension
    src_file = file_url + cif_file
    des_path = file_url + ppath + os.sep
    des_file = des_path + cif_file
    shutil.copyfile(src_file, des_file)
    os.chdir(des_path)
    length = simulation_cell_value(cif_file)
    submit1_sh = ["#!/bin/sh\n",
                  "cd "+ des_path + "\n", 
                  "export RASPA_DIR=/WORK/nscc-gz_material_1/MOFs/sf_box/raspa2/src\n",
                  "#export RASPA_DIR=/WORK/nscc-gz_material_5/Apps/raspa2/src\n",
                  "$RASPA_DIR/bin/simulate\n"
                 ]
    if calculation_mode == "hvf":
        s_hvf_in = ["SimulationType        MonteCarlo\n",
                    "NumberOfCycles        1000\n",
                    "PrintEvery            1000\n",
                    "PrintPropertiesEvery  1000\n",
                    "\n",
                    "Forcefield            UFF4MOFs\n",
                    "ChargeFromChargeEquilibration yes\n",
                    "CutOff                9.8\n",
                    "\n",
                    "Framework 0\n",
                    "FrameworkName" + "     " + str(essential_cif) + "\n",
                    "UnitCells" + "         " + length + "\n",
                    "ExternalTemperature 273.0\n",
                    "\n",
                    "Component 0  MoleculeName             " + "helium" + "\n",
                    "             MoleculeDefinition       TraPPE\n",
                    "             WidomProbability         1.0\n",
                    "             CreateNumberOfMolecules  0\n"
                    ]

        sub_file = "hvf" + str(essential_cif) + ".sh"
        with open("./simulation.input", "w") as f_hvf:
            f_hvf.writelines(s_hvf_in)
        os.chdir(joblist_path)
        with open(r"./" + sub_file, "w") as f_sub:
            f_sub.writelines(submit1_sh)
            
    elif calculation_mode == "ads":
        s_adp_in = ["SimulationType        MonteCarlo\n",
                    "NumberOfCycles        10000\n",
                    "NumberOfInitializationCycles 1000\n"
                    "PrintEvery            1000\n",
                    "PrintPropertiesEvery  1000\n",
                    "\n",
                    "Forcefield            UFF4MOFs\n",
                    "ChargeFromChargeEquilibration yes\n",
                    "CutOff                9.8\n",
                    "\n",
                    "Framework 0\n",
                    "FrameworkName" + "     " + str(essential_cif) + "\n",
                    "UnitCells" + "         " + length + "\n",
                    "ExternalTemperature 273.0\n",
                    "HeliumVoidFraction" + "  hvf_value" + "\n",
                    "ExternalPressure   pressure_value\n",
    
                    "\n",
                    "Component 0  MoleculeName             CO2\n",
                    "             MoleculeDefinition       TraPPE\n",
                    "             TranslationProbability   0.5\n",
                    "             RotationProbability      0.5\n",
                    "             ReinsertionProbability   0.5\n",
                    "             SwapProbability          1.0\n",
                    "             CreateNumberOfMolecules  0\n"
                    ]
        #sub_file = "ads" + str(essential_cif) + ".sh"
        with open("./simulation.input", "w") as f_ads:
            f_ads.writelines(s_adp_in)
        #os.chdir(adsorption_joblist_path)
        #with open(r"./" + sub_file, "w") as f_sub:
        #    f_sub.writelines(submit_sh)
       
    elif calculation_mode == "hc":
        s_hc_in = ["SimulationType        MonteCarlo\n",
                   "NumberOfCycles        10000\n",
                   "NumberOfInitializationCycles 0\n"
                   "PrintEvery            1000\n",
                   "PrintPropertiesEvery  1000\n",
                   "\n",
                   "Forcefield            UFF4MOFs\n",
                   "\n",
                   "Framework 0\n",
                   "FrameworkName" + "     " + str(essential_cif) + "\n",
                   "RemoveAtomNumberCodeFromLabel  yes\n"
                   "UnitCells" + "         " + length + "\n",
                   "ExternalTemperature 77.0\n",
                   "\n",
                   "Component 0  MoleculeName             N2\n",
                   "             MoleculeDefinition       TraPPE\n",
                   "             IdealRosenbluthValue     1.0\n",
                   "             WidomProbability         1.0\n",
                   "             CreateNumberOfMolecules  0\n"
                   ]
        sub_file = "hc" + str(essential_cif) + ".sh"
        with open("./simulation.input", "w") as f_ads:
            f_ads.writelines(s_hc_in)
        os.chdir(joblist_path)
        with open(r"./" + sub_file, "w") as f_sub:
            f_sub.writelines(submit1_sh)
    
    return joblist_path

if __name__ == '__main__':
    import sys
    args = sys.argv
    file_url = args[1]
    calculation_mode = args[2]
    part = args[3]
    work_dir = init_calc_space(file_url)
    for mofpath in work_dir:
        essential_cif = seek_mof_cif(mofpath)
        os.chdir(mofpath)
        calc_cif = babel_cif("".join(essential_cif) + ".cif")
        init_mof_ppcalc(mofpath,calculation_mode,part)
