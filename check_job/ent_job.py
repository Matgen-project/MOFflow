#/usr/bin/env python
import os
import re

def find_job(job_id):
    id = False
    jobcmd = 'squeue | awk \'{print $1}\'' 
    job = os.popen(jobcmd).read()
    id_list = re.split("\n",job)
    if job_id in id_list:
        print('find job ',job_id)
        id = True
    else: 
        print('can not find ',job_id)

    return id        

def get_workdir(job_id):
    dir_cmd = 'yhcontrol show job ' + job_id + ' | grep WorkDir | cut -d "=" -f 2'
    job_dir = os.popen(dir_cmd).read().rstrip()
    script_dir = os.popen('pwd').read().rstrip()
    log = job_dir + os.sep + 'slurm-' + job_id + '.out'
    print("The src dir is:\n",script_dir)
    print("This job dir is:\n",job_dir)
    print("The log file is here:\n",log)
    
    
        

if __name__ == '__main__':
    job_id = input('input job id:')
    if find_job(job_id):
        get_workdir(job_id)
    else:
        exit(1)
        
