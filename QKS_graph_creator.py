import networkx as nx
from sheet_api import *
from random import random


WHYPROB = 1
CONSPROB = 1
HOWPROB = 1
class QKSNode:
    def __init__(self, id, nodetype, title, whyquestion, whyanswer, consquestion, consanswer, howquestion, failednode, code):
        self.id = id
        self.title = title
        self.nodetype = nodetype
        self.whyquestion = whyquestion
        self.whyanswer = whyanswer
        self.consquestion = consquestion
        self.consanswer = consanswer
        self.howquestion = howquestion
        self.failednode = failednode
        self.code = code

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.id == other.id


def createGraph(nodes_sheet, edges_sheet):
    # will create a QKS graphical structure
    G = nx.DiGraph()
    rows = readFromSheet(RANGE=nodes_sheet)
    for row in rows:
        G.add_nodes_from([
            (QKSNode(row[0], row[1], row[3], row[4], row[5],
                     row[7], row[8], row[6], row[9], row[10]), {'type': row[1]})
        ])
    edges = readFromSheet(RANGE=edges_sheet)
    for edge in edges:
        # find the two nodes for the edge
        node1 = [n for n in list(G.nodes) if n.id == edge[1]][0]
        node2 = [n for n in list(G.nodes) if n.id == edge[2]][0]
        G.add_edge(node1, node2, type = edge[0])
    showGraph(G)
    return G

# prints nodes and edges of the graph
def showGraph(G):
    for e in list(G.nodes):
        print(e.title)
    for e in list(G.edges):
        print(e)


def generateNodePairsFromGraph(nodes_sheet, edges_sheet):
    G = createGraph(nodes_sheet=nodes_sheet, edges_sheet=edges_sheet)
    # now generating smart pairs
    # each event node as a question
    nodepairs = []
    for node in list(G.nodes):
        # print(node)
        # print(node.failednode)
        if(node.nodetype == 'GOAL' or node.nodetype == 'EVENT'):
            distance = 0
            path = ''
            createWhyPairs(G, node, node, distance, path, nodepairs)
            if(len(node.consquestion)>0):
                createConsPairs(G, node, node, 0, '', nodepairs)
            if(len(node.howquestion)>0):
                createHowPairs(G, node, node, 0, '', nodepairs)
    nodepairs = reduceNodePairs(nodepairs)
    return nodepairs


#recursive function
def createWhyPairs(G, root, current, distance, path, nodepairs):
    # traverse backward Cs, Os or Is to generate pair
    distance += 1
    for pre in G.predecessors(current):
        if(G[pre][current]['type'] == "C" or G[pre][current]['type'] == "I" or G[pre][current]['type'] == "O+" or G[pre][current]['type'] == "O-"):
            addBeforeChecking({
                 'question': root,
                 'answer': pre,
                 'distance': distance,
                 'path': path + ' backward ' + G[pre][current]['type'],
                 'pairtype': 'Why Question',
                 'code': root.code + pre.code
                 }, nodepairs)
            createWhyPairs(G, root, pre, distance, path+' backward '+ G[pre][current]['type'], nodepairs)
    # traverse forward Rs
    for succ in G.successors(current):
        if(G[current][succ]['type'] == "R"):
            addBeforeChecking({
                'question': root,
                'answer': succ, 
                'distance': distance, 
                'path': path+'forward '+G[current][succ]['type'], 
                'pairtype': 'Why Question',
                'code': root.code + succ.code
                }, nodepairs)
            createWhyPairs(G, root, succ, distance, path+' forward '+G[current][succ]['type'], nodepairs)

def createHowPairs(G, root, current, distance, path, nodepairs):
    #traverse backward Rs, Is to generate pair
    distance += 1
    for pre in G.predecessors(current):
        if(G[pre][current]['type'] == "R") or G[pre][current]['type'] == "I":
            addBeforeChecking({
                 'question': root,
                 'answer': pre,
                 'distance': distance,
                 'path': path + ' backward ' + G[pre][current]['type'],
                 'pairtype': 'How Question',
                 'code': root.code + pre.code
                 }, nodepairs)
            createHowPairs(G, root, pre, distance, path+' backward '+ G[pre][current]['type'], nodepairs)
    
def createConsPairs(G, root, current, distance, path, nodepairs):
    createGoodConsPairs(G, root, current, distance, path, nodepairs)
    createBadConsPairs(G, nodepairs)

#inserts consequence pairs that have ZERO arc distance
def createBadConsPairs(G, nodepairs):
    conslist = [node for node in G if (len(node.consquestion)> 0 and len(node.consanswer) > 0)]
    newnodepairs = [{
            'question': node1,
            'answer' : node2,
            'distance': 99,
            'path': 'NA',
            'pairtype' : 'Comprehension Check',
            'code': node1.code + node2.code
        } 
        for node1 in G 
        for node2 in G 
        if len(node1.consquestion)> 0 and node1 != node2 and len(node2.consanswer)> 0
    ]
    for n in newnodepairs:
        addBeforeChecking(n, nodepairs)


#recursive function
def createGoodConsPairs(G, root, current, distance, path, nodepairs):
    distance += 1
    # traverse forward Rs, Cs, Os or Is
    for succ in G.successors(current):
        if(G[current][succ]['type'] == "R" or G[current][succ]['type'] == "C" or G[current][succ]['type'] == "O+" or  G[current][succ]['type'] == "O-" or G[current][succ]['type'] == "I"):
            if(len(succ.consanswer)>0):
                addBeforeChecking({
                    'question': root, 
                    'answer': succ, 
                    'distance': distance, 
                    'path': path+'forward '+G[current][succ]['type'], 
                    'pairtype': 'Comprehension Check',
                    'code': root.code + succ.code
                    }, nodepairs)
            createGoodConsPairs(G, root, succ, distance, path+' forward '+G[current][succ]['type'], nodepairs)

#checks if same pair of nodes are present in the nodepairs
# retains only the pair that has the lowest distance
def addBeforeChecking(nodepair, nodepairs):
    candidate = [p for p in nodepairs if (p['question'] == nodepair['question'] and p['answer'] == nodepair['answer'] and p['pairtype'] == nodepair['pairtype'])]
    if(len(candidate) == 0):
        nodepairs.append(nodepair)
    elif(candidate[0]['distance']> nodepair['distance']):
        nodepairs.remove(candidate[0])
        nodepairs.append(nodepair)

# there can be different nodes in the graph that represent the same goal/state.
# this method removes the pairs for them, keeping the one with the shortest arc distance    
def reduceNodePairs(nodepairs):
    toremove = []
    for nodepair in list(nodepairs):
        for np in list(nodepairs):
            if(np['question'].title == nodepair['question'].title and np['answer'].title == nodepair['answer'].title and  nodepair['pairtype'] == np['pairtype'] and nodepair != np):
                if(np['distance']>nodepair['distance']):
                    toremove.append(np)
                else:
                    toremove.append(nodepair)
    nodepairs = [n for n in nodepairs if n not in toremove]
    
    toremove = []
    for np in nodepairs:
        if ('Y' in np['question'].failednode or 'Y' in np['answer'].failednode):
            continue
        elif(np['pairtype'] == 'Why Question'):
            #sample with probability for why type questions
            if(random()< (1 - WHYPROB)):
                toremove.append(np)
        elif(np['pairtype'] == 'How Question'):
            #sample with probability for how type questions
            if(random()< (1 - HOWPROB)):
                toremove.append(np)
        else:
            #sample with probability for consequence check questions
            if(random()<(1-CONSPROB)):
                toremove.append(np)
    nodepairs = [n for n in nodepairs if n not in toremove]
    return nodepairs   

def generatePairText(nodepair):
    if(nodepair['pairtype'] == "Why Question"):
        return "Question: " + nodepair['question'].whyquestion + '\n ' + "Answer: " +nodepair['answer'].whyanswer
    elif(nodepair['pairtype'] == "How Question"):
        return "Question: " + nodepair['question'].howquestion + '\n ' + "Answer: " +nodepair['answer'].consanswer
    else:
        return "Question: " + nodepair['question'].consquestion + '\n ' + "Answer: " +nodepair['answer'].consanswer

#print as survey block
def printAsSurveyBlock(pairs, storytext):
    res = ""
    res += "[[Block: Imported From Code]]"
    number = 1
    for pair in pairs:
        res= res + "\n" + str(number) + ". " + storytext + "\n\n " 
        res = res + str(number+1) +". " + str(pair[1])
        res = res + "\n\n " + str(number+2) + ". " + ' Question ' + str(int(number/3) + 1) + ' of ' + str(len(pairs)) + ' Rate this question-answer pair on the scale: ' + "\n\n" 
        res+= "Very Bad Answer \nBad Answer \nGood Answer \nVery Good Answer \n \n [[PageBreak]]"
        number = number + 3 
    return res

def createQAPairs(nodepairs):
    pairs = []
    for i in range(1, len(nodepairs)):
        pairs.append([i,
          generatePairText(nodepairs[i]),
          nodepairs[i]['pairtype'],
          nodepairs[i]['distance'],
          nodepairs[i]['path'],
          nodepairs[i]['code']
          ])
    # for x in range(1, 4):
    #     pairs.append( [i+x,
    #         "Select Good Answer to continue.",
    #         'Comprehension check',
    #         'NA',
    #         'NA',
    #         '0000'
    #     ])
    print('[LOG]Generated ' + str(i-1) + ' questions.' )
    return pairs

def publishPairs(pairs, output_sheet, file_name, storytext):    
    # opening a file in 'w'
    file = open(file_name, 'w')
    file.write(printAsSurveyBlock(pairs, storytext))
    file.close()

    #write to google sheets API
    writeToSheet(body = {
    "values": pairs
    }, SAMPLE_RANGE_NAME=output_sheet)
    print('done')

def setProbs(whyprob, consprob, howprob):
    global WHYPROB , CONSPROB, HOWPROB
    WHYPROB = whyprob
    CONSPROB = consprob
    HOWPROB = howprob

def main():
    nodes_sheet = 'RefillShortNodes!A2:AA2000'
    edges_sheet = 'RefillShortEdges!A2:AA2000' 
    output_sheet = 'Sheet4!A2:AA1000'
    pairs = createQAPairs(generateNodePairsFromGraph(nodes_sheet, edges_sheet))
    publishPairs(pairs, output_sheet, '', '')


# main()
