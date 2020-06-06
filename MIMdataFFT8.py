
import os,time,os.path
import zipfile,csv


import datetime

import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Pool, log_to_stderr,TimeoutError
import time
import random,datetime
import logging,sys




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
    
    #dir2walkthru=r'g:\\data\\ammonite\\'
    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\TAASng\\Atp _MTAA\\T07\\Eblock A\\Eblock A Diskpack 1  Good Stacker B\\'
    #dir2walkthru=r'C:\\Users\\307984\\Documents\\manual\\T1_raw\\test\\'
    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\MX350\\'
    dir2walkthru=r'R:\\data\\Multi_TAA\\auto\\'
    #dir2walkthru=r'C:\\Users\\307984\\Downloads\\Tonia\manual\\'


    ##resultFilelist= GetATSFilesOnPathMSN(dir2walkthru,'csv')
    resultFilelist= GetFilesOnPathOneMDW(dir2walkthru,'csv','csv',1)

    if 1:
    
        file_metrics = open('C:\\Users\\307984\\Downloads\\TAAmetrics23May.csv', 'w')

        for filename in resultFilelist:

                    file_object = open(filename, 'r')
                    
                    # Using readlines() file1 = open('myfile.txt', 'r') 
                    Lines = file_object.readlines()
                    TAAdata=[]
                    for line in Lines[1:]:
                        p=float(line.split(',')[5])
                        TAAdata.append(p)

                    file_object.close()
                    if len(TAAdata)<1000:
                        continue
                    
                    ##FFTMag=4*np.abs(np.fft.fft(TAAdata))/len(TAAdata)
                    FFTMag=np.square(np.abs(np.fft.fft(TAAdata)))
                    FFTMag=FFTMag/len(TAAdata)
                    ##FFTMag=4*np.abs(np.fft.fft(SpiralPESLegacy))/len(SpiralPESLegacy) ##changed in 20April2018 to report P-P, last time is P-0

                    harmonics=[FFTMag[1],FFTMag[2],FFTMag[3],FFTMag[4],FFTMag[22],FFTMag[44],FFTMag[66],FFTMag[88]]
                    #print(["{0:0.2f}".format(i) for i in harmonics])
                    #p=[filename,' ,']+["{0:0.2f}".format(i) for i in harmonics]
                    
                    for k in harmonics:
                        file_metrics.writelines(str(round(k,2)))
                        file_metrics.writelines(',')

                    file_metrics.writelines(','+filename+',');
                    
                    

                    print('FFT harmonics')
                    


                    print(filename)
                    
                    #print(harmonics)
                    plt.close('all');
                    
                    plt.figure();
                    #plt.subplot(1,2,1)
                    x_data=range(0,len(TAAdata))

                    plt.plot(x_data,TAAdata,'b-')
                    plt.plot(TAAdata.index(max(TAAdata)),max(TAAdata),'rd-')
                    plt.plot(TAAdata.index(min(TAAdata)),min(TAAdata),'rd-')
                    plt.xlabel('TAA sample#');plt.ylabel('TAA(mV)');
                    
                    plt.axis([min(x_data),max(x_data),min(TAAdata)-2,max(TAAdata)+2])
                    

                    pos=filename.find('TAA_')
                    str1=filename[0:pos]+'\r\n'+filename[pos:-4]
                    plt.title(filename,fontsize=6)

                    
                    plt.grid(True)
                    idx1=filename.find('_p')
                    str1=filename[idx1-4:idx1]
                    idx1=filename.find('_tk')
                    idx2=filename.find('_4800')
                    str2=filename[idx1:idx2]
                    
                    pos=filename.find('TAA_')
                    
                    p1=filename[0:pos]+str1+str2+'_Plot_'+filename[pos:-4]+'.png'
                    plt.savefig(p1)
                    file_metrics.writelines(','+p1+',');
                    
                    if 1:

                        plt.figure();
                        #plt.subplot(1,2,2)
                        FFTMag[0]=0
                        FFTMag=FFTMag[0:101]
                        x_data=range(0,len(FFTMag))

                        plt.plot(x_data,FFTMag,'b-')
                        plt.xlabel('Harmonics #');plt.ylabel('PSD');
                        
                        
                        plt.axis([min(x_data),max(x_data),0,50])
                        plt.title(filename,fontsize=6)

                        
                        plt.grid(True)
                        pos=filename.find('TAA_')
                        p1=filename[0:pos]+'_FFT_'+filename[pos:-4]+'.png'
                        plt.savefig(p1)
                        file_metrics.writelines(','+p1+',');
                        #pylab.plot(range(1,len(SpiralPESLegacy)),SpiralPESLegacy,'r-',range(1,len(SpiralPESLegacy)),SpiralPESLegacyHarmonicsRemoved,'b-')


                        if False:
                            plt.show(block=False)

                        ##filename=filename.replace('SpiralPESLegacyHarmonicsRemoved','SpiralPESLegacy')
                        ##SavePylabPlotFigure(filename,targetDriveGlobal,'.png')
                    file_metrics.writelines('\r');
            
        file_metrics.close()
