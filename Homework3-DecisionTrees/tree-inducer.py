import csv
import math


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
    entropy = \
        -1 * (numDemocrats/totalReps) * math.log2((numDemocrats/totalReps)) + \
        -1 * (numRepublicans/totalReps) * math.log2((numRepublicans/totalReps))
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


def clipIssue(repSet: list, issue: int) -> list:
    # TODO: clip issue function to remove the issue at given index from all reps
    pass 


if __name__ == "__main__":
    reps = readData("Homework3-DecisionTrees/voting-data.tsv")

    entropy = calculateEntropy(reps)
    print(f"info entropy: {entropy}")

    yae, nae, abstain = seperateIntoSubGroups(reps, 0)
    print(abstain)

    a_entropy = calculateEntropy(abstain)
    print(a_entropy)