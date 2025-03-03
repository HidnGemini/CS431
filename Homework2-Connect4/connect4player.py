"""
This Connect Four player uses magic to choose a move. wowooOOWOOWOowooWOOWOooOWOo
(that's what magic sounds like)

okay in all seriousness, this Connect Four player uses minimax to choose a move.
it is intialized with an ID (whether it is Xs or Os) and a difficulty level, which
is the number of plies to look ahead. 

it's probably worth mentioning that Alex and I compared our minimaxes, and they 
came up with the same results, but were one ply off of each other (my difficulty 
5 was his difficulty 4) and we were also mirrored compared to each other) I mention
this because Silver told me that this was a problem with her's and that you almost 
didn't catch it, so hopefully that helps a little :)
"""
__author__ = "Maddy Stephens"
__license__ = "MIT"
__date__ = "February 2025"

import connect4

# these are really not necessary, but I hate magic numbers so
PLAYER_ONE_VALUE = 1
PLAYER_TWO_VALUE = 2

"""
========================================================================
|||                 TURN OFF ALPHA-BETA PRUNING HERE                 |||
========================================================================
(although I'm quite confident this one actually works!)
"""
PRUNING = True

class ComputerPlayer:
    def __init__(self, id: int, difficulty_level: int):
        """
        Constructor, takes a difficulty level (which indicates the number of 
        plies to look ahead by and a player ID that's  either 1 or 2 that 
        tells the player what its number is.
        """
        self.id = id
        self.difficulty = difficulty_level

    def pick_move(self, rack: tuple) -> int:
        """
        method that is called by connect4.py
        chooses whether to use base minimax or alpha-beta pruning minimax and 
        calls their respective recursive functions with appropriate initial
        arguments
        """
        if PRUNING:
            move, eval = self.calculateAlphaBetaMove(rack, self.difficulty, True, float("-inf"), float("inf"))
        else:
            move, eval = self.calculateMove(rack, self.difficulty, True)
        return move

    def calculateMove(self, rack: tuple, depth: int, isMax: bool) -> tuple:
        """
        recursively decides which move is best according to evalutation function.
        takes a tuple representation of the rack, an integer depth, which is how
        many more plies to go, and a boolean isMax which indicates if this function
        should be a Min call or a Max call.
        """
        move = 1 # initialize move
        # change initial conditions depending on max or min move
        if (isMax):
            playerID = self.id
            evaluation = float("-inf")
        else:
            playerID = PLAYER_ONE_VALUE if self.id == PLAYER_TWO_VALUE else PLAYER_TWO_VALUE
            evaluation = float("inf")

        # if game is over, do not try to continue
        if (ComputerPlayer.isGameOver(rack)):
            return (1, ComputerPlayer.evaluation(self.id, rack))
        
        # loop through each possible move
        for i in range(7):
            hypotheticalBoard = [list(column) for column in rack] # copy board so we can place into it
            if 0 in hypotheticalBoard[i]: # make sure move is legal
                connect4.place_disc(hypotheticalBoard, playerID, i) # place disc on new board
                if depth > 0:
                    # recusion time yippppeeee!!!!!
                    x, boardScore = self.calculateMove(hypotheticalBoard, depth-1, (not isMax))

                else:
                    boardScore = ComputerPlayer.evaluation(self.id, hypotheticalBoard)
                if (not isMax) ^ (boardScore >= evaluation): # the XOR toggles behaviour depending on whether we are doing a min or max move
                    move = i
                    evaluation = boardScore
        return (move, evaluation)
    
    def calculateAlphaBetaMove(self, rack: tuple, depth: int, isMax: bool, alpha: float, beta: float) -> tuple:
        """
        does basically the same thing as calculateMove, but includes an alpha and
        a beta bound for when to quit according to alpha-beta pruning.
        """
        move = 1 # initialize move
        # change initial conditions depending on max or min move
        if (isMax):
            playerID = self.id
            evaluation = float("-inf")
        else:
            playerID = PLAYER_ONE_VALUE if self.id == PLAYER_TWO_VALUE else PLAYER_TWO_VALUE
            evaluation = float("inf")

        # if game is over, do not try to continue
        if (ComputerPlayer.isGameOver(rack)):
            return (1, ComputerPlayer.evaluation(self.id, rack))
        
        # loop through each possible move
        for i in range(7):
            hypotheticalBoard = [list(column) for column in rack] # copy board so we can place into it
            if 0 in hypotheticalBoard[i]: # make sure move is legal
                connect4.place_disc(hypotheticalBoard, playerID, i) # place disc on new board
                if depth > 0:
                    # recusion time yippppeeee!!!!!
                    x, boardScore = self.calculateAlphaBetaMove(hypotheticalBoard, depth-1, (not isMax), alpha, beta)
                    
                    # change alpha-beta pruning behaviour depending on whether its min or max
                    if isMax:
                        # update alpha if this move is better
                        if boardScore > alpha:
                            alpha = boardScore
                    
                        # quit this branch if its already worse than beta
                        if boardScore > beta:
                            return (i, boardScore)
                    else:
                        # quit this branch if its already better than alpha
                        if boardScore < alpha:
                            return (i, boardScore)
                    
                        # update beta if this move is worse (better for min)
                        if boardScore > beta:
                            boardScore = beta
                
                else:
                    boardScore = ComputerPlayer.evaluation(self.id, hypotheticalBoard)
                if (not isMax) ^ (boardScore >= evaluation): # the XOR toggles behaviour depending on whether we are doing a min or max move
                    move = i
                    evaluation = boardScore
        return (move, evaluation)
    
    def isGameOver(rack: tuple) -> bool:
        """
        checks if the game is over by checking if the evaluation function is +-inf
        """
        return (ComputerPlayer.evaluation(1, rack) == float("inf") or ComputerPlayer.evaluation(1,rack) == float("-inf"))

    def evaluation(id, rack: tuple) -> float:
        """
        evaluates a board position by counting number of 1-in-a-rows, 2-in-a-rows, 
        3-in-a-rows, and (shockingly) 4-in-a-rows evaluating them as worth 1,10,100,
        or infinity depending on how many and negating them if they are for the the
        opponent
        """
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
    
    def scoreQuartet(quartet: tuple, modifier: int) -> float:
        """
        scores a quartet in the form of a tuple of length 4. modifier indicates
        whether we are happy for player 1 or happy for player 2.
        """
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