#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
with open("./joblist","r") as f:
    job = f.readlines()
    for line in job:
        jobcode = line
        os.system("yhcancel " + jobcode)
        print(jobcode)
