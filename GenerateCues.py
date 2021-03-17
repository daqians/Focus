# Import libraries
import pandas as pd
import csv
from itertools import zip_longest
import os



# Mandatory function for RapidMiner
def GenerateCues(data):
    # Drop the column 'in documents', that is equal to 'total'
    if ("in documents" in data.columns):
        data.drop("in documents", axis=1, inplace=True)

    # Create the DataFrame used to save the Cues
    cue = pd.DataFrame(columns=["Class", "CueE", "CueER", "CueEC"])

    # Iterate for every column present on data
    for column in data:
        # Checks if the column identify a Class
        if "word" not in column:
            data.rename(index=str, columns={column: str(column + "_123")}, inplace=True)
            column += "_123"

        if (("in class" in column)):
            # Create the new column for the Cue in the input DataFrame, and calculate the values for every Element
            index = data.columns.get_loc(column)-1
            className = "Cue(" + column[10:-5] + ")_123"
            tempColumn = data[column] / data["total_123"]
            data.insert(index, className, tempColumn)

            # Calculate the metrics of that Class
            cue1 = data[className].sum()
            cue2 = cue1 / data[column].sum()
            cue3 = 1 - cue2
            # Save the metrics of that Class
            cue.at[column[10:-5], 'Class'] = column[10:-5]
            cue.at[column[10:-5], 'CueE'] = cue1
            cue.at[column[10:-5], 'CueER'] = cue2
            cue.at[column[10:-5], 'CueEC'] = cue3

    # Calculate the Knowledge metrics of the input
    cue1 = cue["CueE"].sum()
    cue2 = cue1 / data["total_123"].sum()
    cue3 = 1 - cue2
    # Save the Knowledge metrics of the input
    cue.at["CueC", 'Class'] = "CueC,CR,CC"
    cue.at["CueC", 'CueE'] = cue1
    cue.at["CueC", 'CueER'] = cue2
    cue.at["CueC", 'CueEC'] = cue3

    # Return the 4 DataFrames for RapidMiner usage
    return cue, data

# Import libraries


# Mandatory function for RapidMiner
def FCA_lister(matrix):
    data = pd.DataFrame({"word": matrix.columns[3:], "total": 0})
    matrix = matrix.sort_values("Type")
    for index, row in matrix.iterrows():
        colName = "in class (" + row["Type"] + ")"
        data[colName] = 0
        i = 0
        for column in matrix.columns[3:]:
            # If the row has a value, then upload the values of the DataFrame
            if (row[column]):
                data.at[i, colName] = 1
                data.at[i, "total"] = data.at[i, "total"] + 1
            i += 1
    return data

def readFiles(tpath):
    txtLists = os.listdir(tpath)

    return txtLists

def SaveFCAs(path):
    errorlist =[]
    count = 0
    for i in readFiles(path):
        count +=1
        name = i[:-8]
        add = path + i
        a = pd.read_csv(add)
        print(count)
        print("process:", name)
        try:
            lister = FCA_lister(a)
            lister.to_csv("Cue2/%s_Cue_l.csv" % name, index=0)
            Cues,_ = GenerateCues(lister)
            Cues.to_csv("Cue2/%s_Cue.csv" % name, index=0)
        except Exception as e:
            print("Error:",name)
            print(e)
            errorlist.append([name,e])

    print(errorlist)

    
path = 'FCAs-SumUpEtype1/'
SaveFCAs(path)
