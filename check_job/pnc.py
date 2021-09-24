#!/usr/bin/env python
import os
import re
import shutil

def iter_files(root_dir):
    outputfile = []
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            file_name = os.path.join(root,file)
            outfile_extension = ".data"
            path,tmpfilename = os.path.split(file_name)
            #print(tmpfilename)
            filename,extension = os.path.splitext(tmpfilename)
            ads = str(file_name).split("/")[-5]
            if extension == outfile_extension and ads == "Adsorption":
                #print(filename)
                outputfile.append(file_name)

    return outputfile

def confirm_generate(filepath):
    a,b =0,0
    generate = False
    #calc_p_list = ["1e4", "1e5", "2e2", "2e4", "4e4", "5e3", "6e4", "8e4"]
    #calc_p_list = ["5e3","1e4","5e4","1e5","5e5","1e6","1.5e6","2e7"]
    calc_p_list = ["1.5e6","1e4","1e5","1e6","2e7","5e4","5e5","5e7"]
    for i in calc_p_list:
        avp_path = filepath + os.sep + "Adsorption/" + i + os.sep + "Output/System_0/"
        result_path = filepath + os.sep + "Adsorption/" + i + os.sep + "Output"
        try:
            outfile = avp_path + "".join(os.listdir(avp_path))
        except FileNotFoundError:
            src = filepath + os.sep + "Adsorption/" + i 
            generate = False
            des = '/WORK/nscc-gz_material_1/MOFs/jobCheck/notcalc' + os.sep + filepath.split('/')[-1] 
            if not os.path.exists(des):
                os.makedirs(des)
            #mvcmd = 'cp -r  ' + src + ' ' + des
            mvcmd = 'mv  ' + src + ' ' + des
            a+=1
            print('now move uncalc job...\n' + src + ' to \n' + des )
            os.system(mvcmd)
        else:
            generate = True
            if not check_exists_files(outfile):
                src = filepath + os.sep + "Adsorption/" + i 
                des = '/WORK/nscc-gz_material_1/MOFs/jobCheck/notfinished' + os.sep + filepath.split('/')[-1] 
                if not os.path.exists(des):
                    os.makedirs(des)
                #mvcmd = 'cp -r  ' + src + ' ' + des
                mvcmd = 'mv  ' + src + ' ' + des
                os.system(mvcmd)
                print('now move unfinished job...\n' + src + ' to \n' + des )
            else:
                continue 

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
    for mof in mof_result:
        mofpath = mofdir + os.sep + mof
        confirm_generate(mofpath)
