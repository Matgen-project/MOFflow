#!/usr/bin/env python
import os
import time
#sublist = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',\
#           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',\
#           'V', 'W', 'X', 'Y', 'Z']

sublist = ['M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for section in sublist:
    #cmd = 'nohup python resubmit_uncalcjob.py /WORK/nscc-gz_material_1/MOFs/work/MOF_Adsorption/ads_co2_'+section+'/Joblist/ADS  CO2_'+section+'  &'
    #cmd = 'nohup python submit_adsorption_calculation.py /WORK/nscc-gz_material_1/MOFs/data/supplement/N2_77K/calc/part_'+ section + ' ads sup_n2_77k_split16'+ section + ' &'
    cmd = 'nohup yhrun -N 1  python submit_init_calculation.py /WORK/nscc-gz_material_1/MOFs/data/result_hvf_77k/part_'+ section + ' hvf n2_77k_' + section + ' &'
    os.system(cmd)
    time.sleep(5)

exit(0)

