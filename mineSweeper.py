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
    DIM = 3
    #int(input("What dimension should the game board be?\n"))
    MINES = 3
    #int(input("How many mines should be on the game board?\n"))
    SIZE = DIM**2
    SCORE = MINES

    makeGameBoard()
    neighborUpdate()
    printBoardNew()
    agentMove()
    print ("Safe spaces are: {}".format(safeOnes))
    print ("Mines are: {}".format(mineOnes))
    print ("SCORE: {}".format(SCORE))
    print (knowledgeBase)

def printBoard(gameBoard):

    for i in range(len(gameBoard)):
        print(gameBoard["spot{}".format(i)])
    return None


# moves the agent
def agentMove():
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
        print("Agent Move")
        currNum = random.randint(0, SIZE - 1)
        currNumStr = "spot{}".format(currNum)
        # Checking if a space is not selected
        if(not gameBoard[currNumStr]["selected"]):
            # Mark spot as selected
            gameBoard[currNumStr]["selected"] = True
            # If the spot is a mine add to mineOnes and decrease the score
            if (gameBoard[currNumStr].get("isMine")):
                print("YOU'VE HIT A MINE!")
                mineOnes.add(currNum)
                SCORE -= 1
        else: continue

        tempNeighbors = set()
        tempNeighbors = getNeighbors(currNum).symmetric_difference(mineOnes).symmetric_difference(safeOnes)
        tempValue = gameBoard[currNumStr].get("mines") - len(mineOnes.intersection(tempNeighbors))
        knowledgeBase[currNum] = {
            "spots" : tempNeighbors, # neighbhors 
            "value" : tempValue # clue
        }

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
        }"""
                
        logicCheck(currNum)

    return None

#logic check to try and find values of unknown spots
def logicCheck(currNum):
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

    # RULE 4 - 

    # RULE 5 - Remove subsets
    for i in knowledgeBase:
        for j in knowledgeBase:
            #keep = set()
            if knowledgeBase[i]["spots"].issubset(knowledgeBase[j]["spots"]):
                knowledgeBase[j]["spots"].symmetric_difference_update(knowledgeBase[i]["spots"])
    



    """if (gameBoard[currNumStr].get("mines") == 0): # All the neighbors are safe
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
            mineOnes.update(getNeighbors(currNum))"""

    #remove known values from knowledge base
    """for i in knowledgeBase:
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
        
        gameBoard["spot{}".format(i)].update({"mines" : counter})

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

class showMaze():
    def __init__(self):
        global DIM
        global SIZE
        # makes the window for the maze
        window = Tk()
        window.title("Fire Maze")

        # makes the grid all white
        for i in range(SIZE):
            if(GRID[i] == 9):
                color = "red" # path taken
            else:
                color = "white"
            Canvas(window, width=30, height = 30, bg = color).grid(row = i // DIM, column = i % DIM)

        width = 30*DIM*1.20
        height = 30*DIM*1.20
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        window.mainloop()

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
