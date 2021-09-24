#!/usr/bin/env/python
import threading
import re
import os
import linecache
import shutil
import sys

thdmutex = threading.Lock()

class chkthd(threading.Thread):
    def __init__(self, path):
        self.path = path
    def run_job(self,path):
        
     
