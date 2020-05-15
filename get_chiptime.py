# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:54:36 2020

@author: jay
"""

import json
import requests
import pytz
import dateutil
import datetime
from collections import namedtuple
import dateutil.parser
def getChipDate(sequencer):

    url = r"http://ionuser:ionuser@{}/rundb/api/v1/compositeexperiment/".format(sequencer.ip)
    myset = {"limit" : 1, "order_by":"-date" # 只顯示當下最新的 
             }
    
    data = requests.get(url, params = myset )
    jdata = json.loads(data.text)
    #type(jdata["objects"]) list  一個list 是一組實驗
    #type(dataDict) 是 dict
    dataDict = jdata["objects"][0]
    chipDate = dataDict["date"]
    #時間先轉成UTC 再換成台灣
    #dateutil 轉換 "2019-01-24 02:51:35.647011+00:00" -> datetime.datetime(2019, 1, 24, 2, 51, 35, 647011, tzinfo=tzutc()) 

    TW = pytz.timezone(pytz.country_timezones("TW")[0]) #台灣時區
    today = datetime.datetime.today()

    chipDate = dateutil.parser.parse(chipDate)
    taiwan = chipDate.astimezone(TW)
    
    if taiwan.date() == today.date(): # 當上最一片上機日等於當天才回傳日期
        taiwan = (taiwan +  datetime.timedelta(hours=3, minutes=20) if sequencer.name == "S5_A" else taiwan) + datetime.timedelta(minutes=20)
        

        chipDate = taiwan.strftime('%Y-%m-%d %H:%M')
        planName= dataDict["expName"][len(dataDict["expName"])-14:]
        return planName, chipDate


if __name__ == "__main__":
    sequencer = namedtuple("sequencer","ip name")
    sequencerDic = { 
                     "Proton_A" : sequencer("192.168.3.201", "Proton_A"),         
                     "Proton_B" : sequencer("192.168.3.207", "Proton_B"),
                     "S5_A" : sequencer("192.168.3.202", "S5_A"),
                     "S5_B" : sequencer("192.168.3.208", "S5_B")
                     }
    
    for key in sequencerDic:
        if getChipDate(sequencerDic[key]):
            planName, chipDate = getChipDate(sequencerDic[key])
            final = f"{sequencerDic[key].name} {chipDate}"
            print(final)
        else:
            print(f"{sequencerDic[key].name} No Run")
        