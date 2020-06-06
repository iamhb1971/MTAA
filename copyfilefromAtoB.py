
import os,time,os.path
import zipfile,csv


import datetime

import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Pool, log_to_stderr,TimeoutError
import time
import random,datetime
import logging,sys
import shutil


def GetFilesOnPathOneMDW(dir2walkthruLocal, str1,str2,ageLimit):
    resultFilelist1=[]
    timeNow=time.time()
    ageLimit=ageLimit*24*3600.0
    for roots, dirs, files in os.walk(dir2walkthruLocal, topdown=True, onerror=None, followlinks=False):
        for name in files:
            fullpathfilename=os.path.join(roots,name)
            #print(fullpathfilename)
            if fullpathfilename.lower().find(str1.lower())>0:
                if fullpathfilename.lower().find(str2.lower())>0:
                    l=time.localtime(os.path.getmtime(fullpathfilename))
                    ##time.struct_time(tm_year=2018, tm_mon=5, tm_mday=15, tm_hour=18,
                    ##tm_min=32, tm_sec=6, tm_wday=1, tm_yday=135, tm_isdst=0)
                    fileTime=datetime.datetime(l.tm_year,l.tm_mon,l.tm_mday,l.tm_hour,l.tm_min).timestamp()
                    fileAge=timeNow-fileTime
                    #print(fileAge)
                    if fileAge<ageLimit:
                        resultFilelist1.append(fullpathfilename)
                        print(fullpathfilename)
    return resultFilelist1

############################
def GetATSFilesOnPathMSN(dir2walkthru, msn):
    resultFilelist1=[]
    for roots, dirs, files in os.walk(dir2walkthru, topdown=True, onerror=None, followlinks=False):
        for name in files:
            fullpathfilename=os.path.join(roots,name)
            #print(fullpathfilename)
            if fullpathfilename.lower().find(msn.lower())>0:
                    resultFilelist1.append(fullpathfilename)
                    print(fullpathfilename)
                    
                
    return resultFilelist1

if __name__ == '__main__':
    
    #dir2walkthru=r'g:\\data\\ammonite\\'    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\TAASng\\Atp _MTAA\\T07\\Eblock A\\Eblock A Diskpack 1  Good Stacker B\\'
    #dir2walkthru=r'C:\\Users\\307984\\Documents\\manual\\T1_raw\\test\\'
    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\MX350\\'
    dir2walkthru=r'R:\\data\\Multi_TAA\\auto\\'
    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\MX350\\Multi_TAA\\auto\\T15_raw\\'



    resultFilelist= GetFilesOnPathOneMDW(dir2walkthru,'csv','csv',1)

    for item in resultFilelist:
        shutil.copy(item, "C:\\Users\\307984\\Downloads\\111\\")

