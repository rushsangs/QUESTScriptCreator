import csv
import os
import oauth2client

nodes = []
os.chdir(os.path.dirname(__file__))   
with open('sheet.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            nodes.append({'time': row[0], 'node':row[1], 'question': row[2], 'answer': row[3]})


# opening a file in 'w'
file = open('pairs.txt', 'w')

i = 1
for x in filter( lambda a: 'EVENT' in a['node'],nodes) :
    for y in nodes:
        if(x==y or int(y['time']) < int(x['time']) or len(x['question']) <  2):
            continue
        if(x['time'] == y['time'] and 'EVENT' in y['node']):
            continue
        if(y['answer']):
            file.write('PAIR NUMBER: ' + str(i) + '\n')
            i+=1
            file.write(x['question'] + '\n' + y['answer'] + '\n\n')
file.close()
print('generated ' + str(i) + 'questions' )