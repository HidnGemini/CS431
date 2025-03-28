import csv
import math


"""
This classifier is pretty good but I came up with a better one:
Are you Stupid?:
    +R
    -D
    .R
"""

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
            numDemocrats -=- 1
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


def induceTree(trainingSet: list, depth: int, issues: str, outcome: int, parentMajority: str):
    dems, reps = countReps(trainingSet)
    if (len(trainingSet) == 0):
        printIIndents(depth)
        print(f"{groupOrder[outcome]} ", end="")
        print(parentMajority)
        return
    if dems == 0:
        printIIndents(depth)
        print(f"{groupOrder[outcome]} ", end="")
        print("R")
        return
    if reps == 0:
        printIIndents(depth)
        print(f"{groupOrder[outcome]} ", end="")
        print("D")
        return

    bestIssue = findBestSplit(trainingSet, issues)
    newGroups = seperateIntoSubGroups(trainingSet, bestIssue)

    if calculateGain(trainingSet, newGroups) == 0:
        allSame = True
        record = trainingSet[0][2]
        for rep in trainingSet:
            if record != rep[2]:
                allSame = False
                break;
        if allSame:
            printIIndents(depth)
            print(f"{groupOrder[outcome]} ", end="")
            symbol = parentMajority+"**" if reps == dems else "R*" if reps > dems else "D*"
            print(symbol)
            return


    printIIndents(depth)
    print(f"{groupOrder[outcome]} ", end="")
    print(f"Issue {chr(bestIssue+ord('A'))}:")
    #print(f"Issue {bestIssue}")
    issues = clipIndexFromString(issues, issues.index(str(bestIssue)))
    majority = parentMajority if dems == reps else "D" if dems > reps else "R"
    for i,group in enumerate(newGroups):


        # recursive call
        induceTree(group, depth+1, issues, i, majority)


if __name__ == "__main__":
    reps = readData("Homework3-DecisionTrees/voting-data.tsv")
    groupOrder = ("+", "-", ".", "")

    train, tune = splitIntoTrainingAndTuning(reps)

    # bestIssue = findBestSplit(train, issues)
    # print(f"Issue {chr(bestIssue+ord('A'))}:")
    # newGroups = seperateIntoSubGroups(train, bestIssue)
    # issues = clipIndexFromString(issues, bestIssue)
    # for i, group in enumerate(newGroups):
    #     print(f"    {groupOrder[i]} ", end="")
    #     bestIssue = findBestSplit(group, issues)
    #     print(f"Issue {chr(bestIssue+ord('A'))}:")
    induceTree(train, 0, "0123456789", 3, None)

    # string = "0123456789"
    # print(string)
    # string = clipIndexFromString(string, 2)
    # print(string)

    