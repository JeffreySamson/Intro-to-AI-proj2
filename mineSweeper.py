import random
# Mine Sweeper

def main():

    global DIM
    global MINES
    global SIZE
    global gameBoard
    DIM = 10
    #int(input("What dimension should the game board be?\n"))
    MINES = 10
    #int(input("How many mines should be on the game board?\n"))
    SIZE = DIM**2

    
    makeGameBoard()
    #getNeighbors()
    neighborUpdate()


    #print(gameBoard)

def printBoard(gameBoard):

    for i in range(len(gameBoard)):
        print(gameBoard["spot{}".format(i)])
    #print(gameBoard)

    return None

# moves the agent
def agentMove():

    

    return None

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

def neighborUpdate():
    global gameBoard
    global DIM
    for i in range(SIZE):
        neighbors = getNeighbors(i)
        counter = 0
        print(neighbors)
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

    return neighbors

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


#___________________________________________________________________
# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()