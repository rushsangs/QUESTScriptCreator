
from QKS_graph_creator import *
from misc import *

def main():
    ##### DRINK REFILL ####
    #set probabilities for why questions, cons questions and how questions respectively
    setProbs(0.3, 0.1, 0.5)
    longpairs = createQAPairs(generateNodePairsFromGraph("RefillNodes!A2:AA2000", "RefillEdges!A2:AA2000"))
    setProbs(1, 1, 1)
    shortpairs = createQAPairs(generateNodePairsFromGraph("RefillShortNodes!A2:AA2000", "RefillShortEdges!A2:AA2000"))
    newpairs = analyzeAndRandomize(longpairs, shortpairs)
    publishPairs(newpairs['longpairs'], "Sheet3!A1:AA1000", 'longrefill.txt', "Teddy is a bartender working in a bar. He wants to serve a customer their drink. There are bottles of beverage on the shelf. Teddy walks over to the shelf and picks up a bottle. He then attempts to pour a drink from it but fails. He checks the bottle and sees that the bottle is empty. Teddy then places the first bottle back on the shelf and picks up a new bottle. He attempts to pour a drink again and is successful. Teddy then serves the drink to the customer.")
    publishPairs(newpairs['shortpairs'], "Sheet4!A1:AA1000", 'shortrefill.txt', "Teddy is a bartender working in a bar. He wants to serve a customer their drink. There are bottles of beverage on the shelf. Teddy walks over to the shelf and picks up a bottle. He attempts to pour a drink and is successful. Teddy then serves the drink to the customer.")

    ##### BREAKOUT ####
    #set probabilities for why questions, cons questions and how questions respectively
    setProbs(0.3, 0.1, 0.3)
    longpairs = createQAPairs(generateNodePairsFromGraph("BreakoutNodes!A2:AA2000", "BreakoutEdges!A2:AA2000"))
    setProbs(1, 1, 1)
    shortpairs = createQAPairs(generateNodePairsFromGraph("BreakoutShortNodes!A2:AA2000", "BreakoutShortEdges!A2:AA2000"))
    newpairs = analyzeAndRandomize(longpairs, shortpairs)
    publishPairs(newpairs['longpairs'], "Sheet1!A1:AA1000", 'longbreakout.txt', "Dolores is imprisoned inside a jail cell. She wants to escape from the jail. Just outside of the jail cell, there lies a revolver and some bullets on a chair. Dolores walks over and picks up the gun. She walks over to the jail door. Dolores attempts to shoot at the jail door lock but fails. Dolores checks the revolver to see if it is loaded, and finds that it is unloaded. She walks over and picks up the bullets. Dolores loads the bullets into the gun and fires again, this time successfully breaking open the jail door. She then walks out of the jail cell and exits the jail.")
    publishPairs(newpairs['shortpairs'], "Sheet2!A1:AA1000", 'shortbreakout.txt', "Dolores is a cowhand imprisoned inside a cell in the town jail. She wants to escape from the jail. Just outside of the jail cell, a revolver and some bullets sit on a chair. Dolores walks over and picks up the revolver. She walks to the jail door and shoots at the jail door lock, successfully breaking it open. She then walks out of the jail cell and exits the jail.")

main()