import csv
import math


"""
This classifier is pretty good but I came up with a better one:
Are you Stupid?:
    +R
    -D
    .R
"""

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
            return self.parent.getMajority()
        elif self.diff > 0:
            return "D"
        else:
            return "R"
    def __str__(self):
        if self.issue >= 0:
            # question node
            #return f"{self.outcomeSymbol}Issue {chr(self.issue+ord('A'))}:" # convert from issue index to issue name (0->"A", 9->"J")
            return f"{self.outcomeSymbol}Issue {self.issue}"
        else:
            # classification node
            return self.outcomeSymbol + self.getMajority()
    def classify(self, rep):
        print(self)
        if self.issue == -1:
            return self.getMajority()
        else:
            repVote = rep[2][self.issue]
            if repVote == "+":
                return self.positiveChild.classify(rep)
            elif repVote == "-":
                return self.negativeChild.classify(rep)
            elif repVote == ".":
                return self.abstainChild.classify(rep)

def readData(path: str) -> list:
    repSet = [] 
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            repSet.append(row)
    return repSet


def convertToDict(repSet: list) -> dict:
    dict = {}
    for rep in repSet:
        dict[rep[0]] = (rep[1], rep[2])
    return dict


def splitIntoTrainingAndTuning(repSet: list) -> tuple:
    train = []
    tune = []
    for i in range(len(repSet)):
        if i % 4 == 0:
            tune.append(repSet[i])
        else:
            train.append(repSet[i])
    return (train, tune)


def countReps(repSet: list) -> tuple:
    numDemocrats = 0
    numRepublicans = 0

    for rep in repSet:
        if rep[1] == 'D':
            numDemocrats -=- 1 # great way to increment!
        elif rep[1] == 'R':
            numRepublicans -=- 1
        else:
            print(f"WARN: {rep[0]} has a non \"D\" or \"R\" in their party affiliation column!")

    return (numDemocrats, numRepublicans)

 
def calculateEntropy(repSet: list) -> float:
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
    preEntropy = calculateEntropy(group)
    postEntropy = 0;
    for subGroup in subGroups:
        postEntropy += len(subGroup)/len(group)*(calculateEntropy(subGroup))
    return preEntropy-postEntropy


def findBestSplit(repSet: list, issues: str) -> int:
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
    return string[:index]+string[index+1:]


def printIIndents(i: int):
    for j in range(i):
        print("     ", end="")


def induceTree(trainingSet: list, depth: int, issues: str, outcome: int, parentNode: Node):

    dems, reps = countReps(trainingSet)

    # diff is used in Nodes to see how many more democrats there were than republicans
    diff = dems - reps

    if (len(trainingSet) == 0):
        # if trainingSet is empty, classify as parent's majority
        return Node(-1, parentNode.diff, parentNode, None, None, None, groupOrder[outcome])
    elif dems == 0:
        # if there are no democrats in trainingSet, classify as republican
        return Node(-1, -1, parentNode, None, None, None, groupOrder[outcome])
    elif reps == 0:
        # if there are no republicans in the trainingSet, classify as democrat
        return Node(-1, 1, parentNode, None, None, None, groupOrder[outcome])

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
            return Node(-1, diff, parentNode, None, None, None, groupOrder[outcome])
        
    # otherwise, create a new issue node
    thisNode = Node(bestIssue, diff, parentNode, None, None, None, groupOrder[outcome])

    # remove most relevant ussye from issue string
    issues = clipIndexFromString(issues, issues.index(str(bestIssue)))

    # recursive calls yippee i love recursion yippee yay
    thisNode.positiveChild = induceTree(newGroups[0], depth+1, issues, 0, thisNode)
    thisNode.negativeChild = induceTree(newGroups[1], depth+1, issues, 1, thisNode)
    thisNode.abstainChild = induceTree(newGroups[2], depth+1, issues, 2, thisNode)

    return thisNode


def printTree(tree: Node, depth: int):
    printIIndents(depth)
    print(tree)
    if (tree.positiveChild != None): # trees are either leaves or have all the children
        printTree(tree.positiveChild, depth+1)
        printTree(tree.negativeChild, depth+1)
        printTree(tree.abstainChild, depth+1)


def testAccuracy(dataSet: list, tree: Node):
    pass


if __name__ == "__main__":
    reps = readData("Homework3-DecisionTrees/voting-data.tsv")
    groupOrder = ("+ ", "- ", ". ", "")

    train, tune = splitIntoTrainingAndTuning(reps)
    tree = induceTree(train, 0, "0123456789", 3, None)
    printTree(tree, 0)

    #testRep = ['Rep-1', 'D', '.++++.++++']
    #print(f"{testRep[0]} is classified as {tree.classify(testRep)}")

    