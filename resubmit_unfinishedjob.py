#!/usr/bin/env python
import os
import re
import shutil
 
sou_folder = '/WORK/nscc-gz_material_1/MOFs/data/result_hvf_77k'
des_folder = '/WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/calc'
cif_folder = '/WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/cif'
fileinfo = '/WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/ciflist'

resub_list = os.listdir(cif_folder)
for i in resub_list:
    j = os.path.splitext(i)[0]
    with open(fileinfo,"a+") as f1:
        f1.write(j + '\n')
with open(fileinfo,"r") as f2:
    cifinfo = f2.read()
#print(cifinfo) 
for root, dirs, files in os.walk(sou_folder): 
    for file in files:
        if "".join(file).split(".")[-1] == 'data':
            sfile_path=os.path.join(root,file)     
            sfpart = "/".join(sfile_path.split("/")[-6:])
            mofname = sfpart.split("/")[1]
            if mofname in cifinfo:
                sfpath = des_folder + os.sep + "/".join(sfpart.split("/")[:-1])
                if not os.path.exists(sfpath):
                    os.makedirs(sfpath)
                dfile_path= des_folder + os.sep + sfpart
                shutil.copy(sfile_path,dfile_path)
print('moving hvf file was done!\n now start to moving cif file')
path = cif_folder
files_list = os.listdir(path)
for cif_file in files_list:
    filename, suffix = os.path.splitext(cif_file)
    for patnum in (range(65,91) or range(91,123)):
        pat = r"^"+chr(patnum)
        pattren = re.compile(pat)
        matchcif = pattren.match(filename)
        if matchcif is not None:
            filepath = des_folder + "/part_"+"".join(chr(patnum))
            print("Moving  "+ cif_file + "  to  " + filepath + "...")
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            srcfile = path + os.sep  + cif_file
            desfile = filepath + os.sep + cif_file
            shutil.move(srcfile,desfile)
print('done\n now it\'s ok to submit ads job!')
exit(0)
