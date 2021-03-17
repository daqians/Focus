### class of Visualization

import os
import pandas as pd


##loading data
#Make a direction to the temporary file(which is created for generating plots)

class Graph(object):

    def __init__(self, DataFrame):
        self.data = DataFrame
        self.dir = "TemporaryData/"


    #Separate a csv file into target input files
    def sep_file(self):
        headers = self.data.columns.values.tolist()
        num_header = len(headers)
        file_name =[]
        for i in range(len(headers)):
            file_content = self.data[headers[i]].dropna(axis=0,how='all')
            file_n = self.dir + headers[i]+".csv"
            file_content.to_csv(file_n,index=False)
            file_name.append(file_n)
        return file_name,num_header

    #Delete the temporary inputs
    def del_file(self):
        headers = self.data.columns.values.tolist()
        for i in range(len(headers)):
            file_n = self.dir + headers[i] + ".csv"
            if (os.path.exists(file_n)):
                os.remove(file_n)
                print('Removing %s' %file_n)
            else:
                print("The target file is not existing！")

    #The Venn plot function
    def plot_Venn(self,file_name,output,project):
        if 2<=len(file_name)<=6:
            os.system(r"intervene venn -i %s*.csv --output %s --type list --figtype png --fontsize 20 --project %s" %(self.dir,output,project))

    #The UpSet plot function
    def plot_UpSet(self,file_name,output,project):
        if 2 <= len(file_name) <= 6:
            os.system(r"intervene upset -i %s*.csv --output %s --type list --figtype png --project %s" %(self.dir,output,project))

    #The Pairwise plot function
    def plot_Pairwise(self,file_name,output,project):
        if 2 <= len(file_name) <= 30:
            os.system(r"intervene pairwise -i %s*.csv --output %s --type list --figtype png --project %s" %(self.dir,output,project))
    #Function to draw plots
    def DrawGraph(self, output='Results', Gtype='Venn', project = 'Plot'):

        file_name, _ = self.sep_file()
        if Gtype == 'Venn':
            self.plot_Venn(file_name,output,project)
        elif Gtype == 'UpSet':
            self.plot_UpSet(file_name,output,project)
        elif Gtype == 'Pairwise':
            self.plot_Pairwise(file_name,output,project)

        self.del_file()


#example input:
# data = pd.read_csv("Book1.csv")
# g = Graph(data)
# g.DrawGraph(output = 'desktop',Gtype = 'Venn',project = 'plot')
