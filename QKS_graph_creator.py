import networkx as nx
from sheet_api import *

class QKSNode:
    def __init__(self, id, title, whyquestion, whyanswer, consquestion, consanswer, failednode):
        self.id = id
        self.title = title
        self.whyquestion =  whyquestion
        self.whyanswer = whyanswer
        self.consquestion = consquestion
        self.consanswer= consanswer
        self.failednode = failednode

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.id == other.id



def createGraph():
    #will create a QKS graphical structure
    G = nx.DiGraph()
    rows = readFromSheet( RANGE = "Sheet3!A2:AA2000")
    for row in rows:
        G.add_nodes_from([
            (QKSNode(row[0], row[3], row[4], row[5], rows[7], rows[8], rows[9]), {'type': row[1]} )
            ])
    edges = readFromSheet( RANGE = "Sheet3Edges!A2:AA2000")
    for edge in edges: 
        #find the two nodes for the edge
        node1 = [n for n in list(G.nodes) if n.id == edge[1]][0]
        node2 = [n for n in list(G.nodes) if n.id == edge[2]][0]
        G.add_edge(node1, node2, type=edge[0])
    showGraph(G)
    return G

#prints nodes and edges of the graph
def showGraph(G):
    for e in list(G.nodes):
        print(e.title)
    for e in list(G.edges):
        print(e)


def generatePairsFromGraph():
    G = createGraph()
    #now generating smart pairs
    #each event node as a question
    nodetype = nx.get_node_attributes(G, "type")
    # for nodes in list(G.nodes):
    #     if(node)

def main():
    createGraph()

main()