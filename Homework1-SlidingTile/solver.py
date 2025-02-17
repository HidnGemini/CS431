import heapq


class State:
    """
    State class keeps track of information about a certain state of the a puzzle. Instances of
    State are only used in the open list as their information is unnecessary once put onto the
    closed list. Each State instance contains the following information:
        self.puzzle            -  2D tuple reperesentation of the state being tracked.
        self.gapX              -  the X coordinate of the gap; useful to avoid recomputing every time
        self.gapY              -  the Y coordinate of the gap
        self.distanceTraveled  -  the number of moves taken to get to this state
        self.move              -  the move taken to get to this state (of the strings "U", "R", "L", and "D") 
    """
    def __init__(self, puz: list, gapX: int, gapY: int, distanceTraveled: int, move: str):
        """
        State constructor; works as expected except that it takes a list representation of the puzzle
        and converts it rather than expecting a tuple
        """
        self.gapX = gapX
        self.gapY = gapY
        self.distanceTraveled = distanceTraveled
        self.move = move
        self.puzzle = convertToTuple(puz) # deep copy (2D tuple representation)
    def __hash__(self):
        """
        Hash function; ignores all values except for the puzzle's state. Simply uses the built in tuple hash
        """
        return hash(self.puzzle)
    def __lt__(self, other):
        """
        Less than function; this function doesn't need to do anything except for exist as a tiebreaker for the
        priority queue, so it just chooses based on number of moves to get to this state
        """
        return (self.distanceTraveled < other.distanceTraveled)

def solve(puz: list):
    """
    solve function runs A* with whichever heuristic is input below

    ========================================================================
    |||                  CHANGE THE HEURISTIC DOWN HERE                  |||
    ========================================================================
    """
    heuristic = linearConflictHeuristic # this line allows me to easily change the heuristic 
    # options available:
    #   heuristic = ghostTileHeuristic
    #   heuristic = linearConflictHeuristic
    # 
    # explainions for what the heuristics actually do in their respective method headers :)
    # I planned to implement two more (one complicated one I found and the other was the last tile 
    # heuristic that Silver showed me) but I ran out of time due to advanced linear algebra :(

    if (isSolvable(puz)): # if the function isn't solvable, don't bother
        # get puzzle sizes for use later
        height = len(puz)
        width = len(puz[0])

        # find the gap for inputing into state object
        gapX = flatten(puz).index(0) % width
        gapY = flatten(puz).index(0) // width

        # initialize open list and closed list
        closedL = {} # in the form {tuple -> str} where the tuple is the puzzle and the str is one of "U", "D", "L", "R" indicating what move got to that state
        openL = [] # in the form [(int, State)] where the integer is the priority (given by the scoring function and the moves already done)
        
        # push on our initial state
        heapq.heappush(openL, (0 + heuristic(puz), State(puz, gapX, gapY, 0, None)))

        workingPuz = openL[0][1].puzzle # initialize workingPuz field (it doesn't matter what it is since it will be immediately overwritten)
        
        # begin A* loop
        while (not isSolved(workingPuz) and len(openL) != 0): # heapq should never empty entirely unless our isSolvable is broken

            # get new puzzle off heap
            workingState = heapq.heappop(openL)[1]
            workingPuz = convertToList(workingState.puzzle) # allows modification of list as we go

            # if we've already been here, skip this state
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
        return reconstructPath(closedL, workingState.puzzle)
    else:
        return None # CANT DO IT BOSS
    
def reconstructPath(closedL: dict, completedPuz: tuple):
    """
    reconstructPath uses our closedlist dictionary to backtrack what moves were made to get to the solution.
    It loops through, undoing each state in the solution until we've reached our initial state, marked by
    the fact that its "move" field will be None.
    """
    puzzle = convertToList(completedPuz)
    # find gap and make our path string that we append to
    path = ""
    gapY = len(puzzle)-1
    gapX = len(puzzle[0])-1

    # loop back through until we get back to the starting state
    while (closedL[convertToTuple(puzzle)] != None):
        move = closedL[convertToTuple(puzzle)]
        path = move + path
        if (move == "U"):
            # undo up move
            swap(puzzle, gapX, gapY, gapX, gapY-1)
            gapY = gapY-1
        elif (move == "D"):
            # undo down move
            swap(puzzle, gapX, gapY, gapX, gapY+1)
            gapY = gapY+1
        elif (move == "L"):
            # undo left move
            swap(puzzle, gapX, gapY, gapX-1, gapY)
            gapX = gapX-1
        elif (move == "R"):
            # undo right move
            swap(puzzle, gapX, gapY, gapX+1, gapY)
            gapX = gapX+1
        else:
            # this should never happen since the only non "R","L","D","U" is the None on the starting state, but I'm not perfect so this is a good failsafe
            raise Exception("how did you get here?")
    return path
    
def swap(puz: list, x1: int, y1: int, x2: int, y2: int):
    """
    swap swaps the positions of two tiles in the puzzle. This is used to simulate a "move" by usually 
    swapping the empty space with a space adjacent to it.
    """
    temp = puz[y1][x1]
    puz[y1][x1] = puz[y2][x2]
    puz[y2][x2] = temp 
    
def isSolved(puz: list):
    """
    isSolved uses the ghostTileHeuristic function to determine whether the puzzle is solved. If and only
    if the puzzle is solved, ghostTileHeuristic will return 0.
    """
    return (ghostTileHeuristic(puz)==0)

def convertToTuple(puz: list):
    """
    convertToTuple takes a 2d list and converts it to a 2d tuple
    """
    return tuple([tuple(row) for row in puz])

def convertToList(puz: tuple):
    """
    convertToList is the inverse of convertToTuple; taking a 2d tuple and converting it back to a list.
    """
    return list([list(row) for row in puz])

    
def flatten(puz: list):
    """
    flatten takes a 2d array and "flattens" it to a 1d array
    """
    flattened = []
    for row in puz:
        flattened += row
    return flattened

def transpose(puz: list):
    """
    transpose uses a list comprehension to flip the rows and columns of the puzzle. This is only ever
    used for the linear conflict since it is easier to iterate through rows
    """
    return [list(row) for row in zip(*puz)]
    
def ghostTileHeuristic(puz: list):
    """
    ghostTileHeuristic is the basic heuristic outlined in the specs. It pretends all tiles are "ghosts"
    that can slide through each other to get to their positions. This will always underestimate the
    number of moves since the tiles will always have to move at least enough moves to get to their
    spots unobstructed. Formally, this is called the Manhattan Distance, but I came up with ghostTileHeuristic
    and couldn't *not* include that name.
    """
    width = len(puz[0])
    distance = 0
    for i in range(len(puz)):
        for j in range(len(puz[i])):
            elt = puz[i][j]
            if (elt != 0): # ghostTileHeuristic ignores the empty tile
                # subtract one for both of these calculations since we want to one index and put 0 at the end
                eltRow = (elt-1)//width # calculate final row position
                eltCol = (elt-1)%width # calculate final column position
                distance += abs(eltRow-i)
                distance += abs(eltCol-j)
    return distance

def linearConflictHeuristic(puz: list):
    """
    Heuristic described by: https://visualstudiomagazine.com/Articles/2015/10/30/Sliding-Tiles-C-Sharp-AI.aspx?Page=2

    linearConflictHeuristic expands on the Manhattan distance by noting that if two tiles need to move
    through each other (either horizontally or vertically), they will always require (at least) two additional moves. 
    This function uses the Manhattan distance as a base and adds linear conflicts to make the heuristic tighter.
    The heuristic is only admissible if each heuristic is part of one linear conflict. If a tile IS in conflict
    with multiple other tiles, the subsequent conflicts are ignored
    """
    height = len(puz)
    width = len(puz[0])
    score = ghostTileHeuristic(puz) # get the ghost tile heuristic as a base
    # a tile can only be considered in one conflict because solving that conflict could resolve another, so we need to keep track
    conflictingTiles = []

    # look for linear conflicts in rows
    for i in range(len(puz)):
        row = puz[i]
        finalRowContents = [(width*i)+j+1 for j in range(width)] # the last elt will be 1 more than in the puzzle. this would normally correspond to 0, but 0 is never in conflict
        for j in range(len(puz[0])):
            if (row[j] in finalRowContents):
                for k in range(j+1, len(puz[0])):
                    if (row[k]<row[j] and row[k] in finalRowContents and row[j] not in conflictingTiles and row[i] not in conflictingTiles):
                        # if row[k] (which) comes after row[j], is less than row[j] and row[k] is meant to be 
                        # in this row, we have a lkinear conflict so +2 moves minimum (on top of ghost tile)
                        conflictingTiles.append(row[j])
                        conflictingTiles.append(row[k])
                        score += 2
                        break 

    # repeat the same method but for columns (by transposing)
    puzT = transpose(puz)
    for i in range(len(puzT)):
        row = puzT[i]
        finalRowContents = [i+width*j+1 for j in range(height)]
        for j in range(len(puzT[0])):
            if (row[j] in finalRowContents):
                for k in range(j+1, len(puzT[0])):
                    if (row[k]<row[j] and row[k] in finalRowContents and row[j] not in conflictingTiles and row[i] not in conflictingTiles):
                        conflictingTiles.append(row[j])
                        conflictingTiles.append(row[k])
                        score += 2
                        break 

    return score




def isSolvable(puz: list):
    """
    isSolvable uses the algorithm described in the specs to determine whether or not a puzzle is solvable
    """
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
        return (inversions%2 == 0)

if __name__ == "__main__":
    # puzzle = [[6,5,2,3], # given matrix
    #        [0,7,11,4],
    #        [9,1,10,8],
    #        [15,14,13,12]]

    # puzzle = [[1,2,3], # row conflict test case
    #           [7,6,4],
    #           [8,0,5]]

    puzzle = [[1,2,11,4],
              [5,6,8,7],
              [9,10,3,0]] # column conflict test case
    
    # i've had many many other test cases throughout, but I didn't bother to write them anywhere :(
    
    print(solve(puzzle))
