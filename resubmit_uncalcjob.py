#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

args = sys.argv
batchpath = args[1]
section = args[2]
os.chdir(batchpath)
submitpath = "/WORK/nscc-gz_material_1/MOFs/resub/" + section
if not os.path.exists(submitpath):
    os.makedirs(submitpath) 
batch_list = [i for i in os.listdir(batchpath)]
print("total ",len(batch_list))
notsubcounter = 0
for sub in batch_list:
    yhcheckcmd = 'yhacct --name ' + sub + " | awk '{print $6;}' | sed -n \"3, 1p\""
    sub_state = str("".join(os.popen(yhcheckcmd).read()).replace("\n","")).replace(" ","")
    if sub_state == "RNNING" or sub_state == "COMPLETED":
        print("already submitted " ,sub)
        continue
    else:
        notsubcounter += 1
        print("now submitting unfinished job ", sub )
        os.chdir(submitpath)
        os.system("yhbatch -N 1 " + batchpath + os.sep + sub )
        time.sleep(10)
print(notsubcounter)
exit(0)
