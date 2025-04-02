import csv
import math
import sys

"""
This classifier is pretty good but I came up with a better one:
Are you Stupid?:
    +R
    -D
    .R
"""

TREE_SYMBOLS = ("+ ", "- ", ". ", "") # used for printing

class Node:
    def __init__(self, issue: int, diff: int, parent, positiveChild, negativeChild, abstainChild, outcomeSymbol: str):
        # issue corresponds to which issue is being asked about by this node.
        # If this is a classification node, value will be -1
        self.issue = issue
        # diff tells us how many more democrats there were in this group. It will be 
        # positive if the majority was democrats and negative if the majority was 
        # republicans. It will be 0 when there were an equal number of democrats and
        # republicans
        self.diff = diff
        # parent points to this node's parent node
        self.parent = parent
        # positiveChild points to this node's child whose answer to the issue was yae
        self.positiveChild = positiveChild
        # negativeChild points to this node's child whose answer was nae
        self.negativeChild = negativeChild
        # abstainChild points to this node's child whose answer was to abstain
        self.abstainChild = abstainChild
        # outcome symbol is a string used for printing. It will be "" if this is the root,
        # "+ " if this is a positiveChild, "- " if this is a negativeChild, and ". " if this
        # is an abstainChild
        self.outcomeSymbol = outcomeSymbol
    def getMajority(self):
        if self.diff == 0:
            if (self.parent != None):
                return self.parent.getMajority()
            else:
                print("WARN: A branch has no data and therefore cannot get a majority.")
                return "?"
        elif self.diff > 0:
            return "D"
        else:
            return "R"
    def classify(self, rep):
        if (self.issue == -1):
            return self.getMajority()
        else:
            repVote = rep[2][self.issue]
            if repVote == "+":
                return self.positiveChild.classify(rep)
            elif repVote == "-":
                return self.negativeChild.classify(rep)
            elif repVote == ".":
                return self.abstainChild.classify(rep)
    def getNumNodes(self):
        if self.positiveChild == None:
            return 1
        else: 
            return self.positiveChild.getNumberOfNodes() + \
            self.negativeChild.getNumberOfNodes() + \
            self.abstainChild.getNumberOfNodes() + 1
    def __str__(self): 
        if self.issue >= 0:
            # question node
            return f"{self.outcomeSymbol}Issue {chr(self.issue+ord('A'))}:" # convert from issue index to issue name (0->"A", 9->"J")
        else:
            # classification node
            return self.outcomeSymbol + self.getMajority()

def readData(path: str) -> list:
    """
    reads through a file of representative data and returns a
    list of each representative
    """
    repSet = [] 
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            repSet.append(row)
    return repSet


def splitIntoTrainingAndTuning(repSet: list) -> tuple:
    """
    removes every fourth datum from the training set to be used
    for tuning
    """
    train = []
    tune = []
    for i in range(len(repSet)):
        if i % 4 == 0:
            tune.append(repSet[i])
        else:
            train.append(repSet[i])
    return (train, tune)


def countReps(repSet: list) -> tuple:
    """
    counts the number of democrats and the number of republicans
    in the given dataset
    """
    numDemocrats = 0
    numRepublicans = 0

    for rep in repSet:
        if rep[1] == 'D':
            numDemocrats -=- 1 # great way to increment! (i promise i'll stop after this assignment)
        elif rep[1] == 'R':
            numRepublicans -=- 1
        else:
            print(f"WARN: {rep[0]} has a non \"D\" or \"R\" in their party affiliation column!")

    return (numDemocrats, numRepublicans)

 
def calculateEntropy(repSet: list) -> float:
    """
    calculates the information entropy of the given dataset
    """
    numDemocrats, numRepublicans = countReps(repSet)
    totalReps = numDemocrats + numRepublicans
    if numDemocrats != 0 and numRepublicans != 0:
        entropy = \
            -1 * (numDemocrats/totalReps) * math.log2((numDemocrats/totalReps)) + \
            -1 * (numRepublicans/totalReps) * math.log2((numRepublicans/totalReps))
    elif numRepublicans != 0:
        entropy = \
            -1 * (numRepublicans/totalReps) * math.log2((numRepublicans/totalReps))
    elif numDemocrats != 0:
        entropy = \
            -1 * (numDemocrats/totalReps) * math.log2((numDemocrats/totalReps))
    else:
        entropy = 0
    return entropy


def seperateIntoSubGroups(repSet: list, issue: int) -> tuple:
    """
    seperates the given dataset based on given issue and returns
    all three of the subgroups
    """
    yae = []
    nay = []
    abstain = []
    for rep in repSet:
        if rep[2][issue] == '+':
            yae.append(rep)
        elif rep[2][issue] == '-':
            nay.append(rep)
        elif rep[2][issue] == '.':
            abstain.append(rep)
        else:
            print(f"WARN: {rep[0]}'s preferences are incorrectly formatted!")
    return (yae, nay, abstain)


def calculateGain(group: list, subGroups: tuple) -> float:
    """
    calculates the information gain from the given group to the
    given set of subgroups.
    """
    preEntropy = calculateEntropy(group)
    postEntropy = 0;
    for subGroup in subGroups:
        postEntropy += len(subGroup)/len(group)*(calculateEntropy(subGroup))
    return preEntropy-postEntropy


def findBestSplit(repSet: list, issues: str) -> int:
    """
    finds the best issue to split on in the given dataset
    """
    bestIssue = -1
    bestGain = -1
    for issue in issues:
        issue = int(issue)
        subgroups = seperateIntoSubGroups(repSet, issue)
        gain = calculateGain(repSet, subgroups)
        if gain > bestGain:
            bestGain = gain
            bestIssue = issue
    return bestIssue


def clipIndexFromString(string: str, index: int) -> str:
    """
    removes the ith element of a string. This is used internally
    for keeping track of which issues have already been asked about
    """
    return string[:index]+string[index+1:]


def printIIndents(i: int):
    """
    prints an indent i times. pretty self explanatory i think.
    """
    for j in range(i):
        print("     ", end="")


def induceTree(trainingSet: list, issues: str, outcome: int, parentNode: Node):
    """
    recursively induces a decision tree based on the decision tree
    algorithm without any pruning

    all of the parameters 
    """

    dems, reps = countReps(trainingSet)

    # diff is used in Nodes to see how many more democrats there were than republicans
    diff = dems - reps

    if (len(trainingSet) == 0):
        # if trainingSet is empty, classify as parent's majority
        return Node(-1, parentNode.diff, parentNode, None, None, None, TREE_SYMBOLS[outcome])
    elif dems == 0:
        # if there are no democrats in trainingSet, classify as republican
        return Node(-1, -1, parentNode, None, None, None, TREE_SYMBOLS[outcome])
    elif reps == 0:
        # if there are no republicans in the trainingSet, classify as democrat
        return Node(-1, 1, parentNode, None, None, None, TREE_SYMBOLS[outcome])

    # find the best issue to split on and the new resepective groups
    bestIssue = findBestSplit(trainingSet, issues)
    newGroups = seperateIntoSubGroups(trainingSet, bestIssue)

    if calculateGain(trainingSet, newGroups) == 0:
        # if the information gain is 0, check if there are any differences in voting records
        allSame = True
        record = trainingSet[0][2]
        for rep in trainingSet:
            if record != rep[2]:
                allSame = False
                break;
        if allSame:
            # if there are no differences in voting record, classify as majority
            return Node(-1, diff, parentNode, None, None, None, TREE_SYMBOLS[outcome])
        
    # otherwise, create a new issue node
    thisNode = Node(bestIssue, diff, parentNode, None, None, None, TREE_SYMBOLS[outcome])

    # remove most relevant ussye from issue string
    issues = clipIndexFromString(issues, issues.index(str(bestIssue)))

    # recursive calls yippee i love recursion yippee yay
    thisNode.positiveChild = induceTree(newGroups[0], issues, 0, thisNode)
    thisNode.negativeChild = induceTree(newGroups[1], issues, 1, thisNode)
    thisNode.abstainChild = induceTree(newGroups[2], issues, 2, thisNode)

    return thisNode


def printTree(tree: Node, depth: int):
    """
    prints out the tree in the format shown in the specs
    """
    printIIndents(depth)
    print(tree)
    if (tree.positiveChild != None): # trees are either leaves or have all the children
        printTree(tree.positiveChild, depth+1)
        printTree(tree.negativeChild, depth+1)
        printTree(tree.abstainChild, depth+1)


def testAccuracy(dataSet: list, tree: Node) -> float:
    """
    tests accuracy of a given dataset on given tree and returns the
    probability of getting a prediction correct
    """
    total = 0
    correct = 0
    for rep in dataSet:
        classification = tree.classify(rep)
        total -=- 1 # i promise i'll stop after this assignment ;)
        if classification == rep[1]:
            correct -=- 1 # i promise i'll stop after this assignment ;)
    return correct / total


def getAllNonLeafNodes(tree: Node) -> list:
    """
    returns a list of all nodes within a tree by recursively
    traversing the tree
    """
    if tree.positiveChild == None: # trees are either leaves or have all the children
        return []
    positiveChildNodes = getAllNonLeafNodes(tree.positiveChild)
    negativeChildNodes = getAllNonLeafNodes(tree.negativeChild)
    abstainChildNodes = getAllNonLeafNodes(tree.abstainChild)
    return [tree]+positiveChildNodes+negativeChildNodes+abstainChildNodes


def prune(node: Node) -> tuple:
    """
    effectively removes a (non-classification) node by removing the
    pointers to each child, setting its issue to -1 (meaning its
    now a classification node) and returning a tuple of all the data
    removed. This is useful for restoring temporary prunes for testing
    all possible options
    """
    removedData = (node.issue, node.positiveChild, node.negativeChild, node.abstainChild)
    node.issue = -1
    node.positiveChild = None
    node.negativeChild = None
    node.abstainChild = None
    return removedData


def restore(node: Node, removedData: tuple) -> None:
    """
    restores a node to a question node after having been run through
    prune(), taking the node and the return values of prune.
    """
    node.issue = removedData[0]
    node.positiveChild = removedData[1]
    node.negativeChild = removedData[2]
    node.abstainChild = removedData[3]


def pruneWholeTree(tree: Node) -> None:
    """
    prunes the given tree until it cannot be pruned to without hurting
    accuracy.
    """
    notDonePruning = True
    while (notDonePruning):
        # initialize iteration variables
        nodes = getAllNonLeafNodes(tree) 
        nonPrunedAccuracy = testAccuracy(tune, tree)
        bestPrunedAccuracy = -1 # the accuracy will never be negative so this will always be overwritten
        bestPrune = None
        numNodesEliminated = -1

        # try pruning at each node
        for node in nodes:
            removedData = prune(node) # try pruning at node
            newAccuracy = testAccuracy(tune, tree) # test pruned accuracy

            if (newAccuracy > bestPrunedAccuracy) or \
                (newAccuracy == bestPrunedAccuracy) and (node.getNumNodes() > numNodesEliminated): 
                # update if pruned is better than previous prune or 
                # as good and eliminates more nodes
                bestPrune = node
                bestPrunedAccuracy = newAccuracy
                numNodesEliminated = node.getNumNodes()


            restore(node, removedData) # restore pruned node to try nextone
        
        # if our new pruned tree is at least as good, update it. otherwise, we're done pruning
        if bestPrunedAccuracy >= nonPrunedAccuracy:
            prune(bestPrune)   
        else:
            notDonePruning = False 


def estimateAccuracy(dataset: list) -> float:
    """
    estimates the accuracy of this decision tree implementation through
    leave-one-out cross-validaton.
    """
    total = 0
    correct = 0
    for i,datum in enumerate(dataset):
        dataset.remove(datum) # risky to mess with a list while iterating through it! (but its fine hehe)
        
        train, tune = splitIntoTrainingAndTuning(dataset)
        tree = induceTree(train, "0123456789", 3, None)
        pruneWholeTree(tree)
        total -=- 1 # i promise i'll stop after this assignment ;)
        if datum[1] == tree.classify(datum):
            correct -=- 1 # i promise i'll stop after this assignment ;)

        dataset.insert(i, datum) # restore so the for loop doesnt break horribly
    return correct / total


if __name__ == "__main__":
    args = sys.argv
    reps = readData(args[1])

    train, tune = splitIntoTrainingAndTuning(reps)
    tree = induceTree(train, "0123456789", 3, None)

    pruneWholeTree(tree)

    printTree(tree, 0)

    print(f"Approximate Accuracy: {estimateAccuracy(reps)*100}%")

