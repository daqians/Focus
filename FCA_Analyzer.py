### make a statistics of FCA of Schemas


import pandas as pd
import numpy as np
import re
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
import openpyxl
import os

def InfoSchemas(path):
    count = 0
    statistics = pd.DataFrame(columns=['Schema','NProperties','NEntityTypes','Balance','Properties','EntityTypes'])

    for i in readFiles(path):
        count += 1
        name = i[:-4]
        add = "FCAs-SumUpEtype/" + i
        a = pd.read_csv(add)
        print(count)
        print("process:", name)
        try:
            p, e = countPro(a)
            np, ne = len(p), len(e)
            b = Cal_Balance(a)
            new = pd.DataFrame([{'Schema': name, 'NProperties': np, 'NEntityTypes': ne, 'Balance': b,
                                 'Properties': p, 'EntityTypes': e}])

            statistics = statistics.append(new, ignore_index=True)
        except Exception as e:
            print(e)

    statistics.to_csv("Sta_of_FCAs.csv", sep=',', index=0)
    statistics.to_excel('output.xlsx')

def countPro(dataF):
    e = dataF['Type']
    e = list(e)
    p = dataF.columns.values.tolist()
    p = p[2:-1]
    return p,e

def Cal_Balance(schema):
    d = dict()
    for i in range(len(schema)):
        p = schema["Property"][i]
        p = str(p)
        p = p.split()
        p = np.unique(p)
        d['%s' %schema["Type"][i]] = len(p)

    p = [v for v in sorted(d.values())]
    max = p[-1]
    balance = sum(p)/(max*len(d))
    return balance

def readFiles(tpath):
    txtLists = os.listdir(tpath)

    return txtLists


path = "FCAs-SumUpEtype/"
InfoSchemas(path)
