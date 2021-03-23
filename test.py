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
    DIM = 5
    #int(input("What dimension should the game board be?\n"))
    MINES = 4
    #int(input("How many mines should be on the game board?\n"))
    SIZE = DIM**2
    SCORE = MINES

    makeGameBoard()
    neighborUpdate()
    printBoardNew()
    basicAgentMove()
    #reset for advanced agent
    knowledgeBase = {}
    safeOnes = set()
    mineOnes = set()
    SCORE = MINES
    advancedAgentMove()
    #print("FINAL")
    #print ("Safe spaces are: {}".format(safeOnes))
    #print ("Mines are: {}".format(mineOnes))
    #print ( )
    #print ("SCORE: {}".format(SCORE))
    print (knowledgeBase)

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
                #tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                #print("Mines {}".format(gameBoard[currNumStr]["mines"]))
                #print ("Value {}".format(tempValue))
                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)
           # if(selectCheck): break

        
        gameBoard[currNumStr]["selected"] = True
       
        

        """if (not safeOnes):
            currNum = random.randint(0, SIZE - 1)
            while (currNum in mineOnes or gameBoard["spot{}".format(currNum)].get("selected")):
                currNum = random.randint(0, SIZE - 1)
        else:
            currNum = int(safeOnes.pop())

        currNumStr = "spot{}".format(currNum)
        if (gameBoard[currNumStr].get("isMine")):
            print("YOU'VE HIT A MINE!")
            mineOnes.add(currNum)
            SCORE -= 1

        tempNeighbors = set()
        tempNeighbors = getNeighbors(currNum).symmetric_difference(mineOnes).symmetric_difference(safeOnes)
        tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(tempNeighbors))
        knowledgeBase[currNum] = {
            "spots" : tempNeighbors, # neighbhors 
            "value" : tempValue # clue
        }
        """
        print("Picked {}... updating knowlede base".format(currNum))
        print("original value: {}".format(tempValue))
        #updateKnowledgeBase(currNum)
        #if knowledgeBase[currNum]["value"] and knowledgeBase[currNum]["spots"]:
        #    print(knowledgeBase[currNum]["value"])
        #    print(knowledgeBase[currNum]["spots"])
        print ("Mines are: {}".format(mineOnes))
        print ("Safe spots are: {}".format(safeOnes))
        print ("SCORE: {}".format(SCORE))
        print(knowledgeBase)
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
                #tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(unknownNeighbors))
                #print("Mines {}".format(gameBoard[currNumStr]["mines"]))
                #print ("Value {}".format(tempValue))
                knowledgeBase[currNum] = {
                    "spots" : unknownNeighbors, # neighbhors 
                    "value" : tempValue # clue
                }
            updateKnowledgeBase(currNum)
           # if(selectCheck): break
        
        gameBoard[currNumStr]["selected"] = True
       
        

        """if (not safeOnes):
            currNum = random.randint(0, SIZE - 1)
            while (currNum in mineOnes or gameBoard["spot{}".format(currNum)].get("selected")):
                currNum = random.randint(0, SIZE - 1)
        else:
            currNum = int(safeOnes.pop())

        currNumStr = "spot{}".format(currNum)
        if (gameBoard[currNumStr].get("isMine")):
            print("YOU'VE HIT A MINE!")
            mineOnes.add(currNum)
            SCORE -= 1

        tempNeighbors = set()
        tempNeighbors = getNeighbors(currNum).symmetric_difference(mineOnes).symmetric_difference(safeOnes)
        tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(tempNeighbors))
        knowledgeBase[currNum] = {
            "spots" : tempNeighbors, # neighbhors 
            "value" : tempValue # clue
        }
        """
        print("Picked {}... updating knowlede base".format(currNum))
        print("original value: {}".format(tempValue))
        #updateKnowledgeBase(currNum)
        #if knowledgeBase[currNum]["value"] and knowledgeBase[currNum]["spots"]:
        #    print(knowledgeBase[currNum]["value"])
        #    print(knowledgeBase[currNum]["spots"])
        print ("Mines are: {}".format(mineOnes))
        print ("Safe spots are: {}".format(safeOnes))
        print ("SCORE: {}".format(SCORE))
        print(knowledgeBase)
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
                    """elif knowledgeBase[j]["spots"].issubset(knowledgeBase[i]["spots"]):
                        knowledgeBase[i]["spots"].symmetric_difference_update(knowledgeBase[j]["spots"])
                        knowledgeBase[i]["value"].update({"value": knowledgeBase[i]["value"] - (knowledgeBase[j]["value"])})
                        change = True"""


            # RULE 2 - if the value = length of spots then all neighbhors are mines
            if(len(knowledgeBase[i]["spots"]) == knowledgeBase[i]["value"] and len(knowledgeBase[i]["spots"]) != 0):
                mineOnes.update(knowledgeBase[i]["spots"])
                change = True
            
            # RULE 1 - if the value is 0 add all neighbhors to safeOnes
            elif(knowledgeBase[i]["value"] == 0 and len(knowledgeBase[i]["spots"]) != 0):
                safeOnes.update(knowledgeBase[i]["spots"])
                change = True


"""       
    currNumStr = "spot{}".format(currNum)

    # RULE 1 - if the value is 0 add all neighbhors to safeOnes
    if(knowledgeBase[currNum]["value"] == 0):
        safeOnes.update(knowledgeBase[currNum]["spots"])

    # RULE 2 - if the value = length of spots then all neighbhors are mines
    if(len(knowledgeBase[currNum]["spots"]) == knowledgeBase[currNum]["value"]):
        mineOnes.update(knowledgeBase[currNum]["spots"])
    
    # RULE 3 - known mines and safe spaces are removed from the knowledge base and value is updated
    keep = set()
    for i in knowledgeBase[currNum]["spots"]:
        if i not in mineOnes or i not in safeOnes:
            keep.add(i)
        if i in mineOnes:
            knowledgeBase[currNum]["value"] = knowledgeBase[currNum]["value"] - 1
    knowledgeBase[currNum]["spots"] = keep

    # RULE 5 - Remove subsets
    for i in knowledgeBase:
        for j in knowledgeBase:
            #keep = set()
            if knowledgeBase[i]["spots"].issubset(knowledgeBase[j]["spots"]):
                knowledgeBase[j]["spots"].symmetric_difference_update(knowledgeBase[i]["spots"])
 



    if (gameBoard[currNumStr].get("mines") == 0): # All the neighbors are safe
        safeOnes.update(getNeighbors(currNum))
    elif (gameBoard[currNumStr].get("mines") == len(getNeighbors(currNum))): # All the neighbors are mines
        mineOnes.update(getNeighbors(currNum))
    else:
        newNeighbors = getNeighbors(currNum)
        for i in getNeighbors(currNum):
            if (gameBoard["spot{}".format(i)].get("selected")):
                newNeighbors.remove(i)

        if (len(mineOnes.intersection(newNeighbors)) == gameBoard[currNumStr].get("mines")): #All mines are known
            safeOnes.update(getNeighbors.difference(mineOnes))
        elif (len(newNeighbors) == gameBoard[currNumStr].get("mines")): #All the unselected neighbors are mines
            mineOnes.update(getNeighbors(currNum))

    #remove known values from knowledge base
    for i in knowledgeBase:
        keep = set()
        for j in knowledgeBase[i].get("spots"):
            if (j not in mineOnes):
                keep.add(j)
                #tempSpots = knowledgeBase[i].get("spots").remove(j)
                #knowledgeBase[i].update({"spots" : tempSpots}, {"value" : (knowledgeBase[i].get("value") - 1)})
                knowledgeBase[i].update({"value" : (knowledgeBase[i].get("value") - 1)})
            if (j not in safeOnes):
                keep.add(j)
                #tempSpots = knowledgeBase[i].get("spots").remove(j)
                #knowledgeBase[i].update({"spots" : tempSpots})
        knowledgeBase[i].update({"spots" : keep})
    #check for new known values
    for i in knowledgeBase:
        if ((knowledgeBase[i].get("spots"))):
            if (knowledgeBase[i].get("value") == 0):
                safeOnes.add(knowledgeBase[i].get("spots"))
            elif (knowledgeBase[i].get("value") == len(knowledgeBase[i].get("spots"))):
                mineOnes.add(knowledgeBase[i].get("spots"))

    clueChange = True # changes in the clues in order to check again
    while (clueChange):
        #print("Iteration")
        #check if any clues are subsets of other clues
        for i in knowledgeBase:
            for j in knowledgeBase:
                if (i != j):
                    if (knowledgeBase[i].get("spots").issubset(knowledgeBase[j].get("spots"))):
                        knowledgeBase[j].update({"spots" : knowledgeBase[j].get("spots").symmetric_difference(knowledgeBase[i].get("spots"))},
                            {"value" : knowledgeBase[j].get("value") - knowledgeBase[i].get("value")}) # absoloute value
        
        clueChange = False

        #remove known values from knowledge base
        for i in knowledgeBase:
            print("checking for known values")
            keep = set()
            for j in knowledgeBase[i].get("spots"):
                if (j not in mineOnes):
                    keep.add(j)
                    #tempSpots = knowledgeBase[i].get("spots").remove(j)
                    #knowledgeBase[i].update({"spots" : tempSpots},{"value" : (knowledgeBase[i].get("value") - 1)})
                    #clueChange = True
                if (j not in safeOnes):
                    keep.add(j)
                    #tempSpots = knowledgeBase[i].get("spots").remove(j)
                    #knowledgeBase[i].update({"spots" : tempSpots})
                    #clueChange = True
            knowledgeBase[i].update({"spots" : keep})
        
        #check for new known values
        for i in knowledgeBase:
            if (knowledgeBase[i].get("value") == 0):
                safeOnes.update(knowledgeBase[i].get("spots"))
                #clueChange = True
            elif (knowledgeBase[i].get("value") == len(knowledgeBase[i].get("spots"))):
                mineOnes.update(knowledgeBase[i].get("spots"))
                #clueChange = True
    
    #remove accidental duplicates
    safeOnes = list(set(safeOnes))
    mineOnes = list(set(mineOnes))

"""
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

        """# Counting the neighbhor below the target
        if(gameBoard["spot{}".format(i+DIM)].get("isMine")):
            counter += 1
        # Counting the neighbor in the bottom right corner
        if(gameBoard["spot{}".format(i+DIM+1)].get("isMine")):
            counter += 1
        # Counting the neighbor in the bottom left corner
        if(gameBoard["spot{}".format(i+DIM-1)].get(10"isMine")):
            counter += 1
        # Counting the neighbor ito the right
        if(gameBoard["spot{}".format(i+1)].get("isMine")):
            counter += 1
        # Counting the neighbor to the left
        if(gameBoard["spot{}".format(i-1)].get("isMine")):
            counter += 1
        # Counting the neighbor in the bottom left corner
        if(gameBoard["spot{}".format(i+DIM-1)].get("isMine")):
            counter += 1 """
        
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

    print("current:{} and neighbors are {}".format(current, neighborsSet))

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
