#!/usr/bin/env python
import os
import time
import string

partlist = list(string.ascii_uppercase)

for section in partlist:
    #cmd = 'nohup python resubmit_uncalcjob.py /WORK/nscc-gz_material_1/MOFs/work/MOF_Adsorption/ads_co2_'+section+'/Joblist/ADS  CO2_'+section+'  &'
    print('now starting to exract calculation result ',section )
    #cmd = 'nohup python pick_adsorption_result_v1.py /WORK/nscc-gz_material_1/MOFs/data/result_N2/result_ads_N2_77k/part_'+ section + ' N2 '+' &'
    #cmd = 'nohup python pick_adsorption_result_v1.py /WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/calc/part_'+ section + ' N2sup '+' &'
    #cmd = 'nohup yhrun -N 1  python pick_adsorption_result_v1.py /WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/calc/part_'+ section + ' N2sup &'
    #cmd = 'nohup yhrun -N 1  python co2.py /WORK/nscc-gz_material_1/MOFs/data/result_co2/part_'+ section + ' CO2 &'
    cmd = 'nohup yhrun -N 1  python co2.py /WORK/nscc-gz_material_1/MOFs/data/supplement/CO2_sup/calc/part_'+ section + ' CO2sup &'
    os.system(cmd)
    print(cmd)
    time.sleep(1)

exit(0)
