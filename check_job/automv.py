#!/usr/bin/env python
import os
import time
import string

partlist = list(string.ascii_uppercase)

for section in partlist:
    print('now starting to split calculation result ',section )
    #cmd = 'nohup yhrun -N 1  python pnc.py /WORK/nscc-gz_material_1/MOFs/data/result_co2/part_'+ section +' &'
    #cmd = 'nohup yhrun -N 1  python pnc.py /WORK/nscc-gz_material_1/MOFs/data/supplement/CO2_sup/calc/part_'+ section +' &'
    cmd = 'nohup yhrun -N 1  python pnc.py /WORK/nscc-gz_material_1/MOFs/data/supplement/CO2_sup/calc/part_'+ section +' &'
    os.system(cmd)
    print(cmd)
    time.sleep(0.5)

exit(0)
