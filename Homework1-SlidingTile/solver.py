import heapq

class State:
    def __init__(self, puz: list, gapX: int, gapY: int):
        self.gapX = gapX
        self.gapY = gapY
        self.puzzle = tuple([tuple(puz[i]) for i in range(len(puz))]) # deep copy (2D tuple representation)
    def __hash__(self):
        return hash(self.puzzle)

def solve(puz: list):
    if (isSolvable(puz)):
        print("solvable")
        gapX = flatten(puz).index(0) % 4
        gapY = flatten(puz).index(0) // 4
        print(gapX)
        print(gapY)
        height = len(puz)
        width = len(puz[0])
        closed = {0} # zero distinguishes this from a dict (#TODO: maybe fix this hackyness?)
        open = []
        
        heapq.heappush(State(puz, gapX, gapY))

        if (gapX+1<width):
            # left move
            pass
        if (gapX-1>=0):
            # right move
            pass
        if (gapY+1<height):
            # down move
            pass
        if (gapY-1>=0):
            # up move
            pass

    else:
        return None # CANT DO IT BOSS
    

    
def flatten(puz: list):
    flattened = []
    for row in puz:
        flattened += row
    return flattened
    
def ghostTileHeuristic(puz: list):
    height = len(puz)
    width = len(puz[0])
    effectiveGap = height*width # what we treat 0 as
    distance = 0
    for i in range(len(puz)):
        for j in range(len(puz[i])):
            elt = puz[i][j]
            if (elt != 0):
                # subtract one for both these calculations since we want to one index and put 0 at the end
                eltRow = (elt-1)//width 
                eltCol = (elt-1)%height 
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
        return (inversions%2 == 1)

if __name__ == "__main__":
    puzzle = [[6,5,2,3],
           [0,7,11,4],
           [9,1,10,8],
           [15,14,13,12]]

    state1 = State(puzzle, 4)

    solve(puzzle)
