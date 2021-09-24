#!/usr/bin/env python
import os
import re

def iter_files(root_dir):
    outputfile = []
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            file_name = os.path.join(root,file)
            outfile_extension = ".data"
            path,tmpfilename = os.path.split(file_name)
            filename,extension = os.path.splitext(tmpfilename)
            if extension == outfile_extension:
                outputfile.append(file_name)

    return outputfile

def confirm_generate(filepath):
    generate = False
    calc_p_list = ["1e4", "1e5", "2e2", "2e4", "4e4", "5e3", "6e4", "8e4"]
    for i in calc_p_list:
        avp_path = filepath + os.sep + "Adsorption/" + i + os.sep + "Output/System_0/"
        result_path = filepath + os.sep + "Adsorption/" + i + os.sep + "Output"
        try:
            outfile = avp_path + "".join(os.listdir(avp_path))
        except FileNotFoundError:
            generate = False
        else:
            generate = True

    return generate

def check_exists_files(filepath):
    calc = False
    with open(filepath,"r") as f:
        data = f.read()
        #start_check = re.compile(r'Starting simulation')
        start_check = 'Starting simulation'
        #end_check = re.compile(r'Simulation finished,')
        end_check = 'Simulation finished,'
        #if ( start_check.findall(data) and end_check.findall(data) ) is not None:
        if end_check in data:
            calc = True
        else:
            calc = False

    return calc

if __name__ == '__main__':
    import sys
    args = sys.argv
    mofdir = args[1]
    mof_result = os.listdir(mofdir)
    nonf,noncalc = [],[]
    for mof in mof_result:
        mofpath = mofdir + os.sep + mof
        mofoutfile = iter_files(mofpath)
        generate = confirm_generate(mofpath)
        if generate:
            for outfile in mofoutfile:
                calc = check_exists_files(outfile)
                if calc:
                    continue
                else:
                    noncalc.append(mof)
                    print("Calculation Not Finished  ", mof)
                    with open("./nonf","a+") as fnfile:
                        fnfile.writelines(mof + "\n")
        else:
            nonf.append(mof)
            print("No Outfile found  ", mof)
            with open("./noncalc","a+") as fncfile:
                fncfile.writelines(mof + "\n")
    print("Calc Not finished ",len(noncalc))
    print("Not calc ",len(nonf))

