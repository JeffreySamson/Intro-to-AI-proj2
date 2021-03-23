import random
# Mine Sweeper

def main():

    global DIM
    global MINES
    global MINESONES
    global SIZE
    global gameBoard
    global knowledgeBase
    global safeOnes
    global mineOnes
    global agentBoard
    global SCORE
    global MOVE
    gameBoard = {}
    knowledgeBase = {}
    safeOnes = set()
    mineOnes = set()
    MOVE = True
    DIM = int(input("What dimension should the game board be?\n"))
    while(DIM <= 0):
        print("Please enter a positive integer")
        DIM = int(input("What dimension should the game board be?\n"))
    MINES = int(input("How many mines should be on the game board?\n"))
    while(MINES <= 0):
        print("Please enter a positive integer")
        MINES = int(input("How many mines should be on the game board?\n"))
    moveType = int(input("What kind of agent would you like to run? (1 for basic, 2 for advanced)\n"))
    while(moveType != 1 and moveType != 2):
        print("Please enter a 1 or 2")
        moveType = int(input("What kind of agent would you like to run? (1 for basic, 2 for advanced)\n"))
    SIZE = DIM**2
    SCORE = MINES

    makeGameBoard()
    neighborUpdate()
    print("BOARD KEY")
    print("* = mine, 1-8 = clue")
    printBoardNew()
    if(moveType == 1):
        basicAgentMove()
        print("BASIC FINAL")
    elif(moveType == 2):
        advancedAgentMove()
        print("ADVANCED FINAL")
    print ("Safe spaces are: {}".format(safeOnes))
    print ("Mines are: {}".format(mineOnes))
    print ("SCORE: {}".format(SCORE))
    print ( )
    #print (knowledgeBase)

def printBoard(gameBoard):

    for i in range(len(gameBoard)):
        print(gameBoard["spot{}".format(i)])
    return None


# moves the basic agent
def basicAgentMove():
    #RULE 1: If a set is equal to 0, everything in the set is safe
    #RULE 2: If a set is equal to the number of variables in it, everything in the set is a mine
    #RULE 3: Known variables should be removed from all knowledgeBase
    #RULE 4: If you can figure out which members in a set are mines, all others are safe 
    #RULE 5: If there is an intersection, new value is |spotsA - spotsB| = |valueA - valueB|
    global MOVE
    global SIZE
    global MINES
    global SCORE
    global knowledgeBase
    global gameBoard
    global safeOnes
    global mineOnes

    
    while (len(mineOnes) < MINES):
        if(len(safeOnes) + len(mineOnes) == SIZE): break
        currNum = random.randint(0, SIZE - 1)
        currNumStr = "spot{}".format(currNum)
        while(gameBoard[currNumStr].get("selected")):
            currNum = random.randint(0, SIZE - 1)
            currNumStr = "spot{}".format(currNum)
            #print("stuck?")
        # Case for safeOnes being empty
        if not safeOnes:
            if (gameBoard[currNumStr].get("isMine")):
                print("YOU'VE HIT A MINE!")
                mineOnes.add(currNum)
                SCORE -= 1
                tempValue = -1
            else:
                safeOnes.add(currNum)
                unknownNeighbors = getNeighbors(currNum)
                tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                unknownNeighbors = unknownNeighbors.difference(mineOnes).difference(safeOnes)
                if currNum in unknownNeighbors:
                    unknownNeighbors.remove(currNum)
                
                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)
        # Case for safeOnes having some item
        else:
            for i in safeOnes:
                # Checks if i in safeOnes has not been selected
                if not gameBoard["spot{}".format(i)]["selected"]:
                    currNum = i
                    currNumStr = "spot{}".format(currNum)
                    break
            # If all items in safeOnes are selected
            if (gameBoard[currNumStr].get("isMine")):
                print("YOU'VE HIT A MINE!")
                mineOnes.add(currNum)
                SCORE -= 1
                tempValue = -1
            else:
                safeOnes.add(currNum)
                unknownNeighbors = getNeighbors(currNum)
                tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                unknownNeighbors = unknownNeighbors.difference(mineOnes).difference(safeOnes)
                if currNum in unknownNeighbors:
                    unknownNeighbors.remove(currNum)

                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)

        
        gameBoard[currNumStr]["selected"] = True
        if(gameBoard[currNumStr]["isMine"]):
            print("Picked {}... It's a mine... updating knowledge base".format(currNum))
        else:
            print("Picked {}... It's safe... updating knowledge base".format(currNum))
        print("original value: {}".format(tempValue))
        
        if not gameBoard[currNumStr]["isMine"]:
            print("Clue after knowledge base update: {}".format(knowledgeBase[currNum].get("value")))
            print(knowledgeBase[currNum].get("spots"))
        print ("Mines are: {}".format(mineOnes))
        print ("Safe spots are: {}".format(safeOnes))
        print ("CURRENT SCORE: {}".format(SCORE))
        print()

    return None

# moves the advanced agent
def advancedAgentMove():
    #RULE 1: If a set is equal to 0, everything in the set is safe
    #RULE 2: If a set is equal to the number of variables in it, everything in the set is a mine
    #RULE 3: Known variables should be removed from all knowledgeBase
    #RULE 4: If you can figure out which members in a set are mines, all others are safe 
    #RULE 5: If there is an intersection, new value is |spotsA - spotsB| = |valueA - valueB|
    global MOVE
    global SIZE
    global MINES
    global SCORE
    global knowledgeBase
    global gameBoard
    global safeOnes
    global mineOnes

    
    while (len(mineOnes) < MINES):
        if(len(safeOnes) + len(mineOnes) == SIZE): break
        currNum = random.randint(0, SIZE - 1)
        currNumStr = "spot{}".format(currNum)
        if (knowledgeBase):
            tempValueCompare = 9
            tempValueIndex = -1
            for i in knowledgeBase:
                if (knowledgeBase[i].get("value") < tempValueCompare and len(getNeighbors(i).difference(mineOnes).difference(safeOnes)) > 0):
                    tempValueCompare = knowledgeBase[i].get("value")
                    tempValueIndex = i
            
            if (tempValueIndex != -1):
                currNum = getNeighbors(tempValueIndex).difference(mineOnes).difference(safeOnes).pop()
                currNumStr = "spot{}".format(currNum)
            else:
                while(gameBoard[currNumStr].get("selected")):
                    currNum = random.randint(0, SIZE - 1)
                    currNumStr = "spot{}".format(currNum)
        else:
            while(gameBoard[currNumStr].get("selected")):
                currNum = random.randint(0, SIZE - 1)
                currNumStr = "spot{}".format(currNum)
                #print("stuck?")
        # Case for safeOnes being empty
        if not safeOnes:
            if (gameBoard[currNumStr].get("isMine")):
                print("YOU'VE HIT A MINE!")
                mineOnes.add(currNum)
                SCORE -= 1
                tempValue = -1
            else:
                safeOnes.add(currNum)
                unknownNeighbors = getNeighbors(currNum)
                tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                unknownNeighbors = unknownNeighbors.difference(mineOnes).difference(safeOnes)
                if currNum in unknownNeighbors:
                    unknownNeighbors.remove(currNum)
                #tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                #print("Mines {}".format(gameBoard[currNumStr]["mines"]))
                #print ("Value {}".format(tempValue))
                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)
        # Case for safeOnes having some item
        else:
            #selectCheck  = True # var to check if any items in safeOnes haven't been selected yet
            for i in safeOnes:
                # Checks if i in safeOnes has not been selected
                if not gameBoard["spot{}".format(i)]["selected"]:
                    currNum = i
                    currNumStr = "spot{}".format(currNum)
                    break
            # If all items in safeOnes are selected
            #if selectCheck:
            if (gameBoard[currNumStr].get("isMine")):
                print("YOU'VE HIT A MINE!")
                mineOnes.add(currNum)
                SCORE -= 1
                tempValue = -1
            else:
                safeOnes.add(currNum)
                unknownNeighbors = getNeighbors(currNum)
                tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                unknownNeighbors = unknownNeighbors.difference(mineOnes).difference(safeOnes)
                if currNum in unknownNeighbors:
                    unknownNeighbors.remove(currNum)
                
                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)

        
        gameBoard[currNumStr]["selected"] = True
    
        if(gameBoard[currNumStr]["isMine"]):
            print("Picked {}... It's a mine... updating knowledge base".format(currNum))
        else:
            print("Picked {}... It's safe... updating knowledge base".format(currNum))
        print("original value: {}".format(tempValue))
        
        if not gameBoard[currNumStr]["isMine"]:
            print("Clue after knowledge base update: {}".format(knowledgeBase[currNum].get("value")))
            print(knowledgeBase[currNum].get("spots"))
        print ("Mines are: {}".format(mineOnes))
        print ("Safe spots are: {}".format(safeOnes))
        print ("CURRENT SCORE: {}".format(SCORE))
        print()

    return None
    
#logic check to try and find values of unknown spots
def updateKnowledgeBase(currNum):
    #RULE 1: If a set is equal to 0, everything in the set is safe
    #RULE 2: If a set is equal to the number of variables in it, everything in the set is a mine
    #RULE 3: Known variables should be removed from all knowledgeBase
    #RULE 4: If you can figure out which members in a set are mines, all others are safe 
    #RULE 5: If there is an intersection, new value is |spotsA - spotsB| = |valueA - valueB|
    global MOVE
    global SIZE
    global MINES
    global SCORE
    global knowledgeBase
    global gameBoard
    global safeOnes
    global mineOnes
    # Change check
    change = True
    while(change):
        change = False
    # Iterate through the whole knowledge base
        for i in knowledgeBase:
            # Remove from sets any spots in mineOnes and safeOnes
            keep = set()
            for j in knowledgeBase[i]["spots"]:
                if j not in safeOnes and j not in mineOnes:
                    keep.add(j)
                # change value only when mines are removed 
                if j in mineOnes:
                    knowledgeBase[i]["value"] = knowledgeBase[i]["value"] - 1
                
            knowledgeBase[i]["spots"] = keep

            # Simplify if subsets are present
            for j in knowledgeBase:
                if i is not j:
                    if (len(knowledgeBase[i]["spots"]) > 0 and knowledgeBase[i]["spots"].issubset(knowledgeBase[j]["spots"])):
                        knowledgeBase[j]["spots"].symmetric_difference_update(knowledgeBase[i]["spots"])
                        knowledgeBase[j]["value"] = knowledgeBase[j]["value"] - (knowledgeBase[i]["value"])
                        change = True

            # RULE 2 - if the value = length of spots then all neighbhors are mines
            if(len(knowledgeBase[i]["spots"]) == knowledgeBase[i]["value"] and len(knowledgeBase[i]["spots"]) != 0):
                mineOnes.update(knowledgeBase[i]["spots"])
                change = True
            
            # RULE 1 - if the value is 0 add all neighbhors to safeOnes
            elif(knowledgeBase[i]["value"] == 0 and len(knowledgeBase[i]["spots"]) != 0):
                safeOnes.update(knowledgeBase[i]["spots"])
                change = True


# makes the gameboard using the DIM, MINES (number of mines)
def makeGameBoard():
    global DIM
    global MINES
    global SIZE 
    global gameBoard
    gameBoard = {}
    for i in range(SIZE):
        gameBoard["spot{}".format((i))] = {
            "selected" : False,
            "isMine" : False,
            "mines" : 0,
        }

    counter = 0
    while(counter < MINES):
        mineSpot = "spot{}".format(random.randint(0, SIZE - 1))
        if (not gameBoard[mineSpot].get("isMine")):
            gameBoard[mineSpot].update({"isMine": True})
            counter += 1
    
    neighborUpdate()

#get the mine count for each spot
def neighborUpdate():
    global gameBoard
    global DIM
    for i in range(SIZE):
        neighbors = getNeighbors(i)
        counter = 0
        #print(neighbors)
        for j in neighbors:
            if(gameBoard["spot{}".format(j)].get("isMine")):
                counter += 1
        
        if(not gameBoard["spot{}".format(i)].get("isMine")):
            gameBoard["spot{}".format(i)].update({"mines" : counter})
        else:
            gameBoard["spot{}".format(i)].update({"mines" : -1})

#get the valid neighbors to a spot
def getNeighbors(current):
    global SIZE
    global DIM

    left = current - 1
    right = current + 1
    up = current - DIM
    down = current + DIM
    upleft = current - DIM - 1
    upright = current - DIM + 1
    downleft = current + DIM - 1
    downright = current + DIM + 1

    tempNeighbors = [left, right, up, down, upleft, upright, downleft, downright] # all possible neighbors
    neighbors = [] # valid neighbors


    #checks if the current is on the left edges and gets rid of left neighbors
    if (current % DIM == 0):
        tempNeighbors.remove(left)
        tempNeighbors.remove(upleft)
        tempNeighbors.remove(downleft)
    #checks if the current is on the right edges and gets rid of right neighbors
    elif (current % DIM == (DIM - 1)):
        tempNeighbors.remove(right)
        tempNeighbors.remove(upright)
        tempNeighbors.remove(downright)
    #checks if the current is on the down edge and gets rid of down neighbors
    if (current // DIM == (DIM - 1)):
        tempNeighbors.remove(down)
        if (downleft in tempNeighbors):
            tempNeighbors.remove(downleft)
        if (downright in tempNeighbors):
            tempNeighbors.remove(downright)
    #checks if the current is on the top edge and gets rid of top neighbors
    elif(current // DIM == 0):
        tempNeighbors.remove(up)
        if (upleft in tempNeighbors):
            tempNeighbors.remove(upleft)
        if (upright in tempNeighbors):
            tempNeighbors.remove(upright)

    for i in tempNeighbors:
        neighbors.append(i)

    neighborsSet = set()
    for i in range(len(neighbors)):
        neighborsSet.add(neighbors[i])

    return neighborsSet

def printBoardNew():
    global gameBoard
    global DIM

    for i in range(DIM):
        temp = ""
        for j in range(DIM):
            spot = (i * DIM) + j
            if (gameBoard["spot{}".format(spot)].get("isMine")):
                temp += " * "
            else:
                temp += " " + str(gameBoard["spot{}".format(spot)].get("mines")) + " "
                
        print(temp)

#___________________________________________________________________
# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()
