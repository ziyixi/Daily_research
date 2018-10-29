import pandas as pd
import numpy as np
import obspy
from HinetPy import Client, win32
from datetime import datetime, timedelta
import sys

def download_fnet_data(filenames=None,start_times=None,span=22):
    client = Client("xiziyi", "xX1725726868")
    for start_time,filename in zip(start_times,filenames):
        start_time = start_time.datetime+timedelta(hours=9)-timedelta(minutes=2)
        data,ctable=client.get_waveform(code="0103",starttime=start_time,span=span,outdir=filename)
        win32.extract_sac(data, ctable, outdir=filename, with_pz=True)

def getEss():
    catalog=pd.read_table("./download_fnet_me.catalog",sep="\s+",names=["id","date","time","latitude","longitude","depth","magnitude","Mw"])
    catalog["UTCDateTime"]=np.nan
    baseurl="./data/"
    for i in range(catalog.shape[0]):
        catalog.loc[i,"UTCDateTime"]=obspy.UTCDateTime(f"{catalog.loc[i,'date']} {catalog.loc[i,'time']}")
        catalog.loc[i,"id"]=baseurl+catalog.loc[i,"id"]
    return catalog.id.values,catalog.UTCDateTime.values

def main(low,high):
    ids,times=getEss()
    ids=ids[low:high]
    times=times[low:high]
    download_fnet_data(filenames=ids,start_times=times)

if(__name__=="__main__"):
    for i in range(int(sys.argv[1]),int(sys.argv[2])):
        try:
            main(i,i+1)
        except:
            pass