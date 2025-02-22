"""
This Connect Four player just picks a random spot to play. It's pretty dumb.
"""
__author__ = "Maddy Stephens"
__license__ = "MIT"
__date__ = "February 2025"

import random
import time
import connect4

PLAYER_ONE_VALUE = 1
PLAYER_TWO_VALUE = 2

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.difficulty = difficulty_level

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        move, eval = self.maxMove(rack, self.difficulty, "")
        return move
    
    def maxMove(self, rack, depth, soFar):
        move = -1
        eval = float("-inf")
        if (ComputerPlayer.isGameOver(rack)):
            return (-1, ComputerPlayer.evaluation(self.id, rack))
        for i in range(7):
            hypotheticalBoard = [list(column) for column in rack]
            connect4.place_disc(hypotheticalBoard, self.id, i)
            # make sure move is legal
            if 0 in hypotheticalBoard[i]:
                if depth == 3:
                    print(f"[MAX] Trying {soFar}{i}")
                if depth > 0:
                    # recusion time yippppeeee!!!!!
                    x, boardScore = self.minMove(hypotheticalBoard, depth, soFar+str(i))
                else:
                    boardScore = ComputerPlayer.evaluation(self.id, hypotheticalBoard)
                if boardScore >= eval:
                    move = i
                    eval = boardScore
        for i in range(self.difficulty-depth):
            print("    ", end="")
        print(f"[MAX] {soFar}{move} is the best move with score {eval}!")
        return (move, eval)

    def minMove(self, rack, depth, soFar):
        minID = PLAYER_ONE_VALUE if self.id == PLAYER_TWO_VALUE else  PLAYER_TWO_VALUE
        move = -1
        eval = float("inf")
        if (ComputerPlayer.isGameOver(rack)):
            return (-1, ComputerPlayer.evaluation(self.id, rack))
        for i in range(7):
            hypotheticalBoard = [list(column) for column in rack]
            connect4.place_disc(hypotheticalBoard, minID, i)
            # make sure move is legal
            if 0 in hypotheticalBoard[i]:
                #connect4.print_rack(hypotheticalBoard)

                # recusion time yippppeeee!!!!!
                x, boardScore = self.maxMove(hypotheticalBoard, depth-1, soFar+str(i))
                
                if boardScore <= eval:
                    move = i
                    eval = boardScore
        for i in range(self.difficulty-depth+1):
            print("    ", end="")
        print(f"[MIN] {soFar}{move} is the best move with score {eval}!")
        return (move, eval)
    
    def isGameOver(rack):
        return (ComputerPlayer.evaluation(1, rack) == float("inf") or ComputerPlayer.evaluation(1,rack) == float("-inf"))

    def evaluation(id, rack):
        modifier = 1 if id == PLAYER_ONE_VALUE else -1
        score = 0

        # vertical lines
        for col in rack:
            for offset in range(len(col)-3):
                quartet = col[0+offset:4+offset]
                score += ComputerPlayer.scoreQuartet(quartet, modifier)
                        
        # horizontal lines
        for row in zip(*rack):
            for offset in range(len(row)-3):
                quartet = row[0+offset:4+offset]
                score += ComputerPlayer.scoreQuartet(quartet, modifier)

        #positive diagonal lines
        for horizontalIndex in range(len(rack)-3):
            for verticalIndex in range(len(rack)-4):
                quartet = []
                for k in range(4): # pieces of quartet
                    quartet.append(rack[horizontalIndex+k][verticalIndex+k])
                score += ComputerPlayer.scoreQuartet(quartet, modifier)
        
        #negative diagonal lines
        for horizontalIndex in range(len(rack)-3):
            for verticalIndex in range(len(rack)-4):
                quartet = []
                for k in range(4): # pieces of quartet
                    quartet.append(rack[horizontalIndex+3-k][verticalIndex+k])
                score += ComputerPlayer.scoreQuartet(quartet, modifier)
        
        return score
    
    def scoreQuartet(quartet, modifier):
        # are both players not in this quartet?
        if not (PLAYER_ONE_VALUE in quartet and PLAYER_TWO_VALUE in quartet):

            # is only player 1 in quartet?
            if (PLAYER_ONE_VALUE in quartet):
                tokenCount = quartet.count(1)

                if tokenCount == 4:
                    return float('inf') if modifier == 1 else float('-inf')
                else:
                    return modifier*10**(tokenCount-1)

            # is only player 2 in quartet?
            if (PLAYER_TWO_VALUE in quartet):
                tokenCount = quartet.count(2)

                if tokenCount == 4:
                    return float('-inf') if modifier == 1 else float('inf')
                else:
                    return -modifier*(10**(tokenCount-1))
                
            # all 0 row
            else:
                return 0
            
        # row with both players
        else:
            return 0

    def printRack(self,rack):
        for i in range(len(rack[0])):
            for j in range(len(rack)):
                print(rack[j][len(rack[0])-1-i], end=" ")
            print()

if __name__ == "__main__":
    rack = ((1, 1, 0, 0, 0, 0), 
            (0, 0, 0, 0, 0, 0), 
            (0, 0, 0, 0, 0, 0),
            (2, 0, 0, 0, 0, 0), 
            (0, 0, 0, 0, 0, 0), 
            (2, 0, 0, 0, 0, 0), 
            (0, 0, 0, 0, 0, 0))
    #rack = ((42, -1, -2, -3, -4, -5), (-6, -7, -8, -9, 10, 11), (12, 13, 14, 15, 16, 17), (18, 19, 20, 21, 22, 23), (24, 25, 26, 27, 28, 29), (30, 31, 32, 33, 34, 35), (36, 37, 38, 39, 40, 41))
    rack = ((0, 0, 0, 0, 0, 0), 
            (2, 2, 1, 2, 0, 0), 
            (1, 2, 1, 0, 0, 0),
            (1, 1, 2, 2, 0, 0), 
            (1, 0, 0, 0, 0, 0), 
            (2, 1, 1, 1, 2, 0), 
            (0, 0, 0, 0, 0, 0))
    player = ComputerPlayer(2,2)
    player.printRack(rack)
    print(player.maxMove(rack, 3, ""))
