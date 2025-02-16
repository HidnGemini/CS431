import heapq, time

class State:
    def __init__(self, puz: list, gapX: int, gapY: int, distanceTraveled: int, move: str):
        self.gapX = gapX
        self.gapY = gapY
        self.distanceTraveled = distanceTraveled
        self.move = move
        self.puzzle = tuple([tuple(row) for row in puz]) # deep copy (2D tuple representation)
    def __hash__(self):
        return hash(self.puzzle)
    def __lt__(self, other):
        return 1

def solve(puz: list):
    heuristic = ghostTileHeuristic # this line allows me to easily change the heuristic
    if (isSolvable(puz)):
        height = len(puz)
        width = len(puz[0])
        gapX = flatten(puz).index(0) % width
        gapY = flatten(puz).index(0) // height
        closedL = {} # in the form tuple -> str where the tuple is the puzzle and the str is one of "U", "D", "L", "R" indicating what move got here
        openL = []
        
        heapq.heappush(openL, (0 + heuristic(puz), State(puz, gapX, gapY, 0, None)))

        priority, workingState = openL[0] # temporary workaround
        workingPuz = workingState.puzzle
        while (not isSolved(workingPuz)):
            priority, workingState = heapq.heappop(openL)
            workingPuz = convertToList(workingState.puzzle) # allows modification of list as we go
            if (workingState.puzzle not in closedL):
                if (workingState.gapX+1<width):
                    # left move
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX+1, workingState.gapY) # swap to form new puzzle
                    newState = State(workingPuz, workingState.gapX+1, workingState.gapY, workingState.distanceTraveled+1, "L") # create new State object
                    if (not newState.puzzle in closedL.keys()):
                        score = workingState.distanceTraveled+1+heuristic(workingPuz) # compute score for new puzzle
                        heapq.heappush(openL, (score, newState)) # push to priority queue
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX+1, workingState.gapY) # swap back
                if (workingState.gapX-1>=0):
                    # right move
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX-1, workingState.gapY) # swap to form new puzzle
                    newState = State(workingPuz, workingState.gapX-1, workingState.gapY, workingState.distanceTraveled+1, "R") # create new State object
                    if (not newState.puzzle in closedL.keys()):
                        score = workingState.distanceTraveled+1+heuristic(workingPuz) # compute score for new puzzle
                        heapq.heappush(openL, (score, newState)) # push to priority queue
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX-1, workingState.gapY) # swap back
                if (workingState.gapY+1<height):
                    # up move
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX, workingState.gapY+1) # swap to form new puzzle
                    newState = State(workingPuz, workingState.gapX, workingState.gapY+1, workingState.distanceTraveled+1, "U") # create new State object
                    if (not newState.puzzle in closedL.keys()):
                        score = workingState.distanceTraveled+1+heuristic(workingPuz) # compute score for new puzzle
                        heapq.heappush(openL, (score, newState)) # push to priority queue
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX, workingState.gapY+1) # swap back
                if (workingState.gapY-1>=0):
                    # down move
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX, workingState.gapY-1) # swap to form new puzzle
                    newState = State(workingPuz, workingState.gapX, workingState.gapY-1, workingState.distanceTraveled+1, "D") # create new State object
                    if (not newState in closedL.keys()):
                        score = workingState.distanceTraveled+1+heuristic(workingPuz) # compute score for new puzzle
                        heapq.heappush(openL, (score, newState)) # push to priority queue
                    swap(workingPuz, workingState.gapX, workingState.gapY, workingState.gapX, workingState.gapY-1) # swap back
                closedL[workingState.puzzle] = workingState.move # add tuple to closed list (we dont care about anything but the board)
        closedL[workingState.puzzle] = workingState.move # add the final puzzle step to the closed list for reconstruction
        #print(workingState.move)
        #print(workingState.puzzle)
        return reconstructPath(closedL, workingState.puzzle)
    else:
        return None # CANT DO IT BOSS
    
def reconstructPath(closedL: dict, completedPuz: tuple):
    puzzle = convertToList(completedPuz)
    path = ""
    gapY = len(puzzle)-1
    gapX = len(puzzle[0])-1
    while (closedL[convertToTuple(puzzle)] != None):
        #print(path)
        #print(puzzle)
        move = closedL[convertToTuple(puzzle)]
        path = move + path
        if (move == "U"):
            swap(puzzle, gapX, gapY, gapX, gapY-1)
            gapY = gapY-1
        elif (move == "D"):
            swap(puzzle, gapX, gapY, gapX, gapY+1)
            gapY = gapY+1
        elif (move == "L"):
            swap(puzzle, gapX, gapY, gapX-1, gapY)
            gapX = gapX-1
        elif (move == "R"):
            swap(puzzle, gapX, gapY, gapX+1, gapY)
            gapX = gapX+1
        else:
            raise Exception("how did you get here?")
    return path
    
def swap(puz: list, x1: int, y1: int, x2: int, y2: int):
    temp = puz[y1][x1]
    puz[y1][x1] = puz[y2][x2]
    puz[y2][x2] = temp 
    
def isSolved(puz: list):
    return (ghostTileHeuristic(puz)==0)

def convertToTuple(puz: list):
    return tuple([tuple(row) for row in puz])

def convertToList(puz: tuple):
    return list([list(row) for row in puz])

    
def flatten(puz: list):
    flattened = []
    for row in puz:
        flattened += row
    return flattened
    
def ghostTileHeuristic(puz: list):
    height = len(puz) # should be 3
    width = len(puz[0]) # should be 4
    effectiveGap = height*width # what we treat 0 as
    distance = 0
    for i in range(len(puz)):
        for j in range(len(puz[i])):
            elt = puz[i][j]
            
            if (elt != 0):
                # subtract one for both these calculations since we want to one index and put 0 at the end
                eltRow = (elt-1)//width
                eltCol = (elt-1)%width
                distance += abs(eltRow-i)
                distance += abs(eltCol-j)
    return distance

def isSolvable(puz: list):
    # set up flattened list
    width = len(puz[0])
    flattened = flatten(puz)
    gapPosition = flattened.index(0)
    flattened.remove(0)

    # count inversions
    inversions = 0
    for i in range(len(flattened)):
        for j in range(i+1, len(flattened)):
            if flattened[i] > flattened[j]:
                inversions-=-1 # unfortunately I'm FORCED to do this since python doesn't have ++
        
    # check width and perform necessary changes
    if (width%2==0):
        inversions += len(puz)-(gapPosition//4) - 1
        return (inversions%2 == 0)
    else:
        print(inversions)
        return (inversions%2 == 0)

if __name__ == "__main__":
    puzzle = [[6,5,2,3],
           [0,7,11,4],
           [9,1,10,8],
           [15,14,13,12]]
#     1 2 3 4
# . 5 6 7
# 9 10 11 8
    puzzle = [[1,2,3,4],
              [0,5,6,7],
              [9,10,11,8]]

    solve(puzzle)
