import csv
import os
from sheet_api import *
from random import random
from QKS_graph_creator import createGraph

def printAsSurveyBlock(pairs):
    res = ""
    res += "[[Block: Imported From Code]]"
    for pair in pairs:
        res+= "\n" + str(pair[0]) +". " + pair[1] + "\n\n" 
        res+= "Very Bad Answer \nBad Answer \nGood Answer \nVery Good Answer \n"
    return res

def GeneratePairsFromSpreadsheet():
    # reads the data from the Google Sheet spreadsheet
    # indices: 0- time step, 1- node, 2- why question, 
    # 3- why answer, 4- how question, 5- consequence question, 
    # 6- consequence answer, 7- Critical flag
    
    #current probability: 
    # 50 percent chance of including a non-critical comprehension question
    # 30 percent chance of including a non-critical why question
    nodes = readFromSheet( RANGE = "A2:AA2000")

    pairs = []
    i = 1
    for x in filter( lambda a: 'EVENT' in a[1],nodes) :
        for y in nodes:
            if(x==y or int(y[0]) < int(x[0]) or len(x[2]) <  2):
                #same time step or X occurs after Y, skip
                continue
            if(x[0] == y[0] and 'EVENT' in y[1]):
                # same time step and both are event nodes
                continue
            try:
                if('EVENT' in y[1] and x[5] and len(x[5])>2 and  y[6] and len(y[6])>2):
                    if('Y' in y[7] or 'Y' in x[7]):
                        pairs.append([i, x[5] + '\n' + y[6], 'Comprehension check'])
                    elif(random() < 0.5): 
                        pairs.append([i, x[5] + '\n' + y[6], 'Comprehension check'])

            except IndexError:
                pass
           
            if(y[3]):
                if('Y' in y[7] or 'Y' in x[7]):
                    pairs.append([ i,  x[2] + '\n' + y[3], 'WHY'])
                    i+=1
                elif(random() < 0.5 ): 
                    pairs.append([ i,  x[2] + '\n' + y[3], 'WHY'])
                    i+=1
    
    # opening a file in 'w'
    file = open('pairs.txt', 'w')
    file.write(printAsSurveyBlock(pairs))
    file.close()
    print('[LOG]Generated ' + str(i-1) + ' questions.' )

    # write to google sheet
    writeToSheet(body = {
    "values": pairs
    }, SAMPLE_RANGE_NAME="A2:AA1000")


def generatePairsFromGraph():
    G = createGraph()
    
def main():
    GeneratePairsFromSpreadsheet()


main()