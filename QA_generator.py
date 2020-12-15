import csv
import os
from sheet_api import *


# reads the data from the Google Sheet spreadsheet
nodes = readFromSheet( RANGE = "A2:AA2000")


# nodes = []
# os.chdir(os.path.dirname(__file__))   
# with open('sheet.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count += 1
#         else:
#             line_count += 1
#             nodes.append({'time': row[0], 'node':row[1], 'question': row[2], 'answer': row[3]})


# opening a file in 'w'
file = open('pairs.txt', 'w')

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
            file.write('PAIR NUMBER: ' + str(i) + '\n')
            i+=1
            file.write(x[2] + '\n' + y[3] + '\n\n')
file.close()
print('generated ' + str(i) + ' questions' )

# write to google sheet
writeToSheet(body = {
  "values": pairs
}, SAMPLE_RANGE_NAME="A2:AA1000")