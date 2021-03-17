import pandas as pd
import csv
from itertools import zip_longest
import os
import math

def readFiles(tpath):
    txtLists = os.listdir(tpath)

    return txtLists

def atan(x):
    b = []
    for i in x:
        bb = ( math.atan(i) * 2 / math.pi)
        b.append(bb)
    b = pd.Series(b)
    return b

def log(x,maxx):
    b = []
    for i in x:
        bb = math.log10(i+1)/math.log10(maxx)
        b.append(bb)
    b = pd.Series(b)
    return b

def SaveFCAs(path):
    errorlist = []
    count = 0
    FreqC, FreqCR, FreqE, FreqER = find_max_freq()
    print(FreqC, FreqCR, FreqE, FreqER)
    CueC, CueCR, CueE, CueER, mCueE, mCueER, mCueC, mCueCR = find_max_cue()
    print(CueC, CueCR, CueE, CueER)
    print( mCueC, mCueCR, mCueE, mCueER)
    f = 1
    sta_schemas = pd.DataFrame(
        columns=["Schema", "nClass", "CueE_n", "CueER_n", "FreqE_n", "FreqER_n", 'search', 'share', 'overall'])

    for i in readFiles(path):
        if 'csv' not in i:
            continue
        count += 1
        name = i[:-8]
        add1 = 'Cue/%s_Cue.csv' %name
        add2 = 'Freq/%s_Freq.csv' %name
        cue = pd.read_csv(add1)
        # cue = cue.sort_values("Class")
        freq = pd.read_csv(add2)
        # freq = freq.sort_values("Class")
        overallS = pd.DataFrame(columns=["Class", "CueE", "CueE_n", "CueER", "CueER_n", 'FreqE', 'FreqE_n','FreqER', 'FreqER_n','search','share','overall'])
        cue = cue.fillna(0)
        freq = freq.fillna(0)

        print(count)
        print("process:", name)

        try:
            l = cue.shape[0]
            overallS['Class'] = cue['Class'][0:-1]
            overallS.at["overall", 'Class'] = "Overall"

            overallS['CueE'] = cue['CueE']
            overallS['CueE_n'] = (cue['CueE'][0:-1]-mCueE)/(CueE-mCueE) if f == 0 else log(cue['CueE'][0:-1],CueE)
            overallS.at["overall", 'CueE_n'] = math.log10(cue['CueE'][l-1]+1)/math.log10(CueC)
            overallS['CueER'] = cue['CueER']
            overallS['CueER_n'] = (cue['CueER'][0:-1]-mCueER)/(CueER-mCueER)
            overallS.at["overall", 'CueER_n'] = cue['CueER'][l-1]/CueCR

            overallS['FreqE'] = freq['FreqE']
            overallS['FreqE_n'] = freq['FreqE'][0:-1]/FreqE if f== 0 else log(freq['FreqE'][0:-1],FreqE)
            overallS.at["overall", 'FreqE_n'] = math.log10(freq['FreqE'][l-1]+1)/math.log10(FreqC)
            overallS['FreqER'] = freq['FreqER']
            overallS['FreqER_n'] = freq['FreqE'][0:-1]/FreqER
            overallS.at["overall", 'FreqER_n'] = freq['FreqER'][l-1]/FreqCR

            overallS['search'] = (overallS['CueER_n'] + overallS['CueE_n'])/2
            overallS['share'] = (overallS['FreqER_n'] + overallS['FreqE_n'])/2
            overallS['overall'] = (overallS['search'] + overallS['share'])/2

            overallS.to_csv('OverallScore2/%s.csv' %name, index=0)

            sta_schemas.at['%s' % name, 'Schema'] = name
            sta_schemas.at['%s' % name, 'nClass'] = overallS.shape[0]-1
            sta_schemas.at['%s' % name, 'CueE_n'] = overallS.at["overall", 'CueE_n']
            sta_schemas.at['%s' % name, 'CueER_n'] = overallS.at["overall", 'CueER_n']
            sta_schemas.at['%s' % name, 'FreqE_n'] = overallS.at["overall", 'FreqE_n']
            sta_schemas.at['%s' % name, 'FreqER_n'] = overallS.at["overall", 'FreqER_n']
            sta_schemas.at['%s' % name, 'search'] = overallS.at["overall", 'search']
            sta_schemas.at['%s' % name, 'share'] = overallS.at["overall", 'share']
            sta_schemas.at['%s' % name, 'overall'] = overallS.at["overall", 'overall']

        except Exception as e:
            print("Error:", name)
            print(e)
            errorlist.append([name, e])
    sta_schemas.to_csv("sta_schemas.csv", index=0)



def find_max_freq():
    FreqE, FreqER = 0, 0
    FreqC, FreqCR = 0, 0
    path1 = 'Freq/'
    for i in readFiles(path):
        if 'csv' not in i:
            continue
        add = path1 + i[0:-7] +'Freq.csv'
        a = pd.read_csv(add,index_col='Class')
        a = a.fillna(0)
        if a.at['FreqC,CR,CC','FreqE'] > FreqC:
            FreqC = a.at['FreqC,CR,CC','FreqE']
        if a.at['FreqC,CR,CC','FreqER'] > FreqCR:
            FreqCR = a.at['FreqC,CR,CC','FreqER']

        if a['FreqE'][0:-1].max() > FreqE:
            FreqE = a['FreqE'][0:-1].max()
        if a['FreqER'][0:-1].max() > FreqER:
            FreqER = a['FreqE'][0:-1].max()
    return FreqC, FreqCR, FreqE, FreqER

def find_max_cue():
    CueE, CueER = 0, 0
    CueC, CueCR = 0, 0
    mCueE, mCueER = 999, 999
    mCueC, mCueCR = 999, 999
    path1 = 'Cue/'
    for i in readFiles(path):
        if 'csv' not in i:
            continue
        add = path1 + i[:-7] + 'Cue.csv'
        a = pd.read_csv(add,index_col='Class')
        a = a.fillna(0)
        if a.at['CueC,CR,CC','CueE'] > CueC:
            CueC = a.at['CueC,CR,CC','CueE']
        if a.at['CueC,CR,CC','CueER'] > CueCR:
            CueCR = a.at['CueC,CR,CC','CueER']

        if a.at['CueC,CR,CC','CueE'] < mCueC:
            mCueC = a.at['CueC,CR,CC','CueE']
        if a.at['CueC,CR,CC','CueER'] < mCueCR:
            mCueCR = a.at['CueC,CR,CC','CueER']

        if a['CueE'][0:-1].max() > CueE:
            CueE = a['CueE'][0:-1].max()
        if a['CueER'][0:-1].max() > CueER:
            CueER = a['CueER'][0:-1].max()

        if a['CueE'][0:-1].min() < mCueE:
            mCueE = a['CueE'][0:-1].min()
        if a['CueER'][0:-1].min() < mCueER:
            mCueER = a['CueER'][0:-1].min()
    return CueC, CueCR, CueE, CueER, mCueE, mCueER, mCueC, mCueCR

path = 'FCAs-SumUpEtype1/'
SaveFCAs(path)