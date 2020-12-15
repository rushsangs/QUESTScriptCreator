import csv
import os
from sheet_api import *

def printAsSurveyBlock(pairs):
    res = ""
    res += "[[Block: Imported From Code]]"
    for pair in pairs:
        res+= "\n" + str(pair[0]) +". " + pair[1] + "\n\n" 
        res+= "Very Bad Answer \nBad Answer \nGood Answer \nVery Good Answer \n"
    return res

def main():
    # reads the data from the Google Sheet spreadsheet
    nodes = readFromSheet( RANGE = "A2:AA2000")

    

    pairs = []
    i = 1
    for x in filter( lambda a: 'EVENT' in a[1],nodes) :
        for y in nodes:
            if(x==y or int(y[0]) < int(x[0]) or len(x[2]) <  2):
                continue
            if(x[0] == y[0] and 'EVENT' in y[1]):
                continue
            if(y[3]):
                pairs.append([ i,  x[2] + '\n' + y[3]])
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


main()