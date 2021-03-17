### visualization of three kinds of statistics

import pandas as pd
import numpy as np
import openpyxl
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import os
from InterVenn import Graph
import random


def readFiles(tpath):
    txtLists = os.listdir(tpath)

    return txtLists

def GetEtypes(dataframe):
    d = pd.DataFrame(index=range(10000))
    a = ['FreeBase','OpenCyc-Light','dbpedia-owl','SUMO','schema']
    for i in a:
        d['%s' %i]=dataframe['%s' %i]
    print(d)
    return d

def Venn4allEtypes1(path):
    try:
        result = pd.read_csv("VennSet4AllEtypesToSchemas1/Venn4allEtypes1.csv")
        print('reading')
        print(result)
    except:

        result = pd.DataFrame(index=range(30000))
        for file_name in readFiles(path):
            try:
                name = file_name[:-8]
                add = path + file_name
                a = pd.read_csv(add)
                print("process:", name)
                e = a['Type']
                result["%s" %name] = e
            except Exception as ee:
                print(file_name,ee)

        result.to_csv("VennSet4AllEtypesToSchemas1/Venn4allEtypes1.csv",index=False)

    e = GetEtypes(result)
    return e


def find_most_shared_DType(dataframe):
    try:
        df = pd.read_csv('VennSet4AllPropertyToSchemas2/FCA_of_Schemas_Etypes.csv',index_col='Schema')
        print('reading')
        print(df)
    except:
        d = GetEtypes(dataframe)
        dd = dict()
        for i, j in d.iteritems():
            s = " "
            print(i)
            j = j.dropna(axis=0, how='any')
            j = list(j)
            k = s.join(j)
            dd['%s' % i] = k

        Corpus = [pros for _, pros in dd.items()]
        Entities = [pros for pros, _ in dd.items()]
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(Corpus)
        x = X.toarray()
        x = x.T
        names = vectorizer.get_feature_names()
        df = pd.DataFrame()
        df["Schema"] = Entities
        for k in range(len(x)):
            df['%s' % names[k]] = x[k]

        df = df.append([{'Schema': 'sum'}], ignore_index=True)
        df = df.append([{'Schema': 'Schemas'}], ignore_index=True)
        df = df.set_index('Schema')
        index_of_schemas = dict({0:'FreeBase',1:'OpenCyc-Light',2:'dbpedia-owl',3:'SUMO',4:'schema'})
        for i, j in df.iteritems():
            df.loc['sum', '%s' % i] = j.sum()
            index = []
            s = ' '
            for jj in range(5):
                if j[jj] == 1 :
                    index.append(index_of_schemas[jj])
            df.loc['Schemas', '%s' % i] = s.join(index)
        df.to_csv('VennSet4AllPropertyToSchemas2/FCA_of_Schemas_Etypes.csv')

    result = []
    for i,j in df.iteritems():
        if j.loc['sum'] == '5.0': ##'3.0' and '4.0' and '5.0'
            result.append([i,j.loc['Schemas']])
    print(result)
    return result

def Venn4singleEtypes2(path):
    data = pd.read_csv('VennSet4AllEtypesToSchemas1/Venn4allEtypes1.csv')
    Etypes = find_most_shared_DType(data)

    for item in Etypes:
        try:
            PlotData = pd.read_csv('VennSet4AllPropertyToSchemas2/%s.csv' %item[0])
        except:
            kk = item[1].split(' ')
            PlotData = pd.DataFrame(index=range(1000))
            for i in kk:
                add = path + i + '_FCA.csv'
                d = pd.read_csv(add,index_col='Type')
                k = d.loc['%s' %item[0]]
                PlotData['%s' %i] = GetProperties(k)
            PlotData.to_csv('VennSet4AllPropertyToSchemas2/%s.csv' %item[0],index=False)

        print(PlotData)
        g = Graph(PlotData)
        g.DrawGraph(output='VennSet4AllPropertyToSchemas2', Gtype = 'Venn', project = item[0])


def GetProperties(dataframe):
    l = []
    for i,j in dataframe.iteritems():
        try:
            if int(j) > 0:
                l.append(i)
        except:
            continue
    l = pd.Series(l)
    print(l)
    return l

def find_most_shared_property_of_Dtype(dataframe,item):
    #横向做和
    d = dict()
    for i in range(len(dataframe)):
        n = str(dataframe['Property'][i]).split(' ')
        n = len(n)
        t = dataframe.index
        d['%s' % t[i]] = n

    d = sort_by_value(d)
    r = [item]
    for i in d:
        if i[1] !=item:
            r.append(i[1])
        elif i[1] ==item:
            continue
    r = r[0:5]

    results = pd.DataFrame(index=range(1000))
    for i in r:
        i = str(i)
        p = dataframe.loc['%s' % i, 'Property']
        p = p.split(' ')
        p = pd.Series(p)
        results['%s' % i] = p
    return results

def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return backitems[0:5]

def Venn4allEtypes3(path):
    data = pd.read_csv('VennSet4AllEtypesToSchemas1/Venn4allEtypes1.csv')
    Etypes = find_most_shared_DType(data)

    for item in Etypes:
        kk = item[1].split(' ')
        for i in kk:
            PlotData = pd.DataFrame(index=range(1000))
            add = path + i + '_FCA.csv'
            d = pd.read_csv(add, index_col='Type')
            name = i + '_' + item[0]
            try:
                PlotData = pd.read_csv('VennSet4AllPropertyAcrossEtypes3/%s.csv' % item[0])
            except:
                k = find_most_shared_property_of_Dtype(d,item[0])
                for j in k.columns:
                    kj = k.loc[:, '%s' % j]
                    PlotData['%s' % j] = kj
                PlotData.to_csv('VennSet4AllPropertyAcrossEtypes3/%s.csv' % name, index=False)

            g = Graph(PlotData)
            g.DrawGraph(output='VennSet4AllPropertyAcrossEtypes3', Gtype='Venn', project=name)
    return
def VennGenerator(path,f):
    try:
        if f == '1':
            x = Venn4allEtypes1(path)
            g = Graph(x)
            g.DrawGraph(output='VennSet4AllEtypesToSchemas1',Gtype='Venn')

        elif f == '2':
            Venn4singleEtypes2(path)

        elif f == '3':
            Venn4allEtypes3(path)

    except Exception as e:
        print(e)

path = "FCAs-SumUpEtype/"
VennGenerator(path,'3')
