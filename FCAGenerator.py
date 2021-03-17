#### generate FCAs by schemas
import pandas as pd
import numpy as np
import re
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
import os

#Flitering Properities in triples and list them
def GetET_P(triples):
    # Create the DataFrame to save the vocabs' triples with the predicates present on the argument 'predicates'
    df = pd.DataFrame(columns=["Type", "Property", "FCATerms"])

    # Get the list of predicates
    strPredicates = ["domain", "domainIncludes"] #"domainIncludes"

    # Return all the triples if there is no predicate filtering
    if(len(strPredicates) == 0):
        df["Type"] = triples["Object"]
        df["Property"] = triples["Subject"]
        return df


    # Iterate for every predicate
    for pred in strPredicates:
        # Create the list used to add the triples that has that predicate
        list_ = list()
        index_ = 0
        # Iterate for every triples present on the file passed on the argument 'triples'
        for index, row in triples.iterrows():
            # if a triple has a specified PredicateTerm or the predicates are not set
            if(row["Predicate"] == pred):
                # Save that triple on the list
                t = replace(row["Object"])
                x = replace(row["Subject"])
                t = t.replace("_", "")
                t = t.replace(" ", "")
                list_.insert(index_,{"Type": t, "Property": row["Subject"],"FCATerms": x})
                index_ += 1
        # Save the information on the list to the DataFrame for each predicate checked
        if(index_ and len(list_)):
            df = df.append(list_)

    # Return the DataFrame for RapidMiner usage
    return df

#Clean the Properity Terms
def replace(prop):
    x = str(prop)
    #Fliter specific codes out
    C = ['ERO','OBI','BFO','IAO','RO','SWO','ERO','ARG']
    for c in C:
        if c in prop:
            return x
    #Fliter Numbers

    #Fliter Dashes
    # x =x.replace('-','')

    #Fliter upper cases

    r = re.compile('[A-Z]*[a-z]*[_]*\d*')
    x = " ".join(r.findall(x))
    x = x.lower().strip()
    return x

#Tokenize Properity Terms and make FCA matrix
def WordVect(dataframe):
    # Stop words and Tokenization

    #if need sum up all properties of one entity
    #xx = GetCorpus(dataframe)

    #if generate FCA directly
    for i in range(len(dataframe)):
        text = dataframe['FCATerms'][i].split()
        for j in range(len(text)):
            text[j] = text[j].replace("_","")
            text[j] = text[j].strip()
        filtered_words = [word for word in text if word not in get_stop_words('english') and not word.isdigit()]
        if len(filtered_words) > 0:
            dataframe['FCATerms'][i] = " ".join(filtered_words)
        else:
            dataframe['FCATerms'][i] =np.nan

    dataframe = dataframe.dropna(axis=0, how='any')


    #one-hot word embedding
    # df = pd.DataFrame(columns=["Type", "Property", "FCATerms"])
    corpus = [pros for pros in dataframe['FCATerms']]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    x = X.toarray()
    x = x.T
    names = vectorizer.get_feature_names()
    for k in range(len(x)):
        dataframe['%s' % names[k]] = x[k]
    return dataframe

#Get the corpus and preparing for one-hot word embedding
def GetCorpus(dataframe):
    d = dict()
    for i in range(len(dataframe)):
        if dataframe["Type"][i] in d:
            d['%s' % dataframe["Type"][i]] += ' ' + dataframe["FCATerms"][i]
        elif dataframe["Type"][i] not in d:
            d['%s' % dataframe["Type"][i]] = dataframe["FCATerms"][i]
    for k, v in d.items():
        text = v.split()
        for i in range(len(text)):
            text[i] = text[i].replace("_","")
            text[i] = text[i].strip()
        filtered_words = [word for word in text if word not in get_stop_words('english') and not word.isdigit()]
        d[k] = " ".join(filtered_words)


    Corpus = [pros for _, pros in d.items() if len(pros)>0]
    Entities = [pros for pros, _ in d.items() if len(_)>0]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(Corpus)
    x = X.toarray()
    x = x.T
    names = vectorizer.get_feature_names()
    df = pd.DataFrame()
    df["Type"] = Entities
    df["Property"] = Corpus
    NCorpus = []
    for i in Corpus:
        i = str(i).split(' ')
        NCorpus.append(len(i))
    df["NProperty"] = NCorpus
    for k in range(len(x)):
        df['%s' % names[k]] = x[k]

    return df

def readFiles(tpath):
    txtLists = os.listdir(tpath)

    return txtLists

def SaveFCAs(path,f):
    errorlist =[]
    count = 0
    for i in readFiles(path):
        count +=1
        name = i[:-4]
        add = "LastVersion/" + i
        a = pd.read_csv(add)
        print(count)
        print("process:", name)
        try:
            x = GetET_P(a)
            if f == 'single':
                xx = WordVect(x)
                xx.to_csv("FCAs-singleEtype1/%s_FCA.csv" %name,index=0)
            elif f == 'sum':
                xx = GetCorpus(x)
                xx.to_csv("FCAs-SumUpEtype1/%s_FCA.csv" % name, index=0)
        except Exception as e:
            print("Error:",name)
            print(e)
            errorlist.append([name,e])

    print(errorlist)

path = 'LastVersion/'
SaveFCAs(path,'single')



