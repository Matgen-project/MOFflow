#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import argparse
import re
import os

parser = argparse.ArgumentParser("modefiy cif files")
parser.add_argument("jobpath", help="job check path")
args = parser.parse_args()
jbp = args.jobpath

num, qnum = 0, 0

mutex = threading.Lock()
class mythread(threading.Thread):
    def __init__(self, cf):
        super(mythread, self).__init__()
        self.cf = cf

    def run_job(self):
        global num,qnum
        if mutex.acquire(1):
            chk = chkcf(self.cf)
            wnum = get_lines_cf(self.cf)

            if chk:
                num += 1
                print(self.cf, "Already modify ", num, " file")
            if wnum == 1:
                qnum += 1
                print("got it %d！, wrong cif line! %s" % (qnum, self.cf))
            mutex.release()

def findcf(jbp):
    ciflist = []
    for root, list_dirnames, list_filenames in os.walk(jbp):
        for file in list_filenames:
            if os.path.splitext(file)[-1] == ".cif":
                fn = os.path.join(root, file)
                ciflist.append(fn)

    return ciflist

def chkcf(cf):
    chk = False
    cfname = os.path.split(cf)[-1]
    pat = re.compile(r"#END")
    with open(cf, "r") as f:
        data = f.read()
    findstr = pat.findall(data)

    if len(findstr) > 1:
        print(findstr)
        print("find it ", cfname, " now starting modify...")
        modata = data.split("#END")[0]
        #os.rename(cf, cfname + "_wrong_cif")
        with open(cf, "w") as f2:
            f2.write(modata + "\n#END")
        chk = True

    return chk

def get_lines_cf(cf):
    with open(cf, "r") as f:
        data = f.readlines()
    wnum = len(data)

    return wnum

cflist = findcf(jbp)

thd_list = []

for cf in cflist:
    t = mythread(cf)
    t.start()
    thd_list.append(t)

for mythd in thd_list:
    mythd.run_job()

print("Total chk cif ",len(thd_list))
print("Total wrong cif ",qnum)
print("Total muti-end cif ",num)

print("GG, well done!")
