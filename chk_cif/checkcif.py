#!/usr/bin/env python
import re
import os
import linecache
import shutil
import sys

args = sys.argv
srcpath = args[1]
#despath = args[2]
#srcpath = "/WORK/nscc-gz_material_1/MOFs/data/cif/all_cif"
#despath = "/WORK/nscc-gz_material_1/MOFs/data/cif/changecif" 
#if not os.path.exists(despath):
#    os.makedirs(despath)
files = [ i for i in os.listdir(srcpath) if os.path.splitext(i)[1] == ".cif"]
pbfile = []
print(len(files))
pat = re.compile(r"#END")
for file in files:
    with open(srcpath + os.sep + file,"r") as f:
        data = f.read()
    findstr = pat.findall(data)
    if len(findstr) != 1:
        print(findstr)
        print("find it ",file," now starting modeify...")
        modata = data.split("#END")[0]
        #print(modata)
        os.system('mv ' + file + ' wrong_cif' )
        with open(srcpath + os.sep + file,"w") as f2:
            f2.write(modata + "\n#END")
        pbfile.append(file)
        srcfile = srcpath + os.sep + file
        #desfile = despath + os.sep + file
        #shutil.copy(srcfile,desfile)
print(len(pbfile)," edited")

     

