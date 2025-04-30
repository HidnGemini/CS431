import sys
import csv
import numpy as np
from operator import add

# constant used for converting from "+--+.+" notation into a vector
VOTE_MEANING = {
    '+': 1,
    '-': -1,
    '.': 0
}

class Representative:
    """
    Representative class; holds representative name, party, and voting 
    record as a vector
    """
    def __init__(self, rep):
        """
        sets id, party, and coordinateVector by calling findCoordinates
        """
        self.id = rep[0]
        self.party = rep[1]
        self.coordinateVector = Representative.findCoordinates(rep[2])
    def findCoordinates(votingRecord):
        """
        uses VOTE_MEANING constant dictionary to convert from 
        "+,-, and ." to "1, -1, and 0" respectively in a vector
        """
        return [VOTE_MEANING.get(vote) for vote in votingRecord]


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


def makeRepresentativeList(repData):
    """
    converts raw data read in by readData and converts them into 
    Representative objects.
    """
    representativeList = []
    for rep in repData:
        representativeList.append(Representative(rep))
    return representativeList


def getSquaredDistance(coords1, coords2):
    """
    finds the squared euclidean distance between the two input
    vectors
    """
    differences = np.subtract(coords1, coords2) # subtract the two vectors elt-wise
    differences = [i**2 for i in differences]
    return sum(differences)


def findFarthestReps(representativeList):
    """
    find the two representatives that are farthest away from
    each other
    """
    maxDistRepsIndex = (-1, -1)
    maxDist = -1
    for i in range(len(representativeList)):
        for j in range(len(representativeList)):
            # check if ith and jth representatives are the most distant so far
            dist = getSquaredDistance(representativeList[i].coordinateVector, representativeList[j].coordinateVector)
            if dist > maxDist:
                maxDist = dist
                maxDistRepsIndex = (i, j)
    return maxDistRepsIndex


def makeInitialCentroids(representativeList, numCentroids):
    """
    takes a list of representatives and finds the initial centroid
    points by setting the two farthest candidates as the first 2
    and then setting each other centroid to the farthest from
    all other centroids
    """
    index1, index2 = findFarthestReps(representativeList)
    centroidIndices = [index1, index2]

    for i in range(numCentroids-2):
        # for every centroid after the first two:
        maxDist = -1
        maxInd = 0
        for j in range(len(representativeList)):
            # find the sum of distances
            sumOfSquaredDist = 0
            for k in range(len(centroidIndices)):
                sumOfSquaredDist += getSquaredDistance(representativeList[j].coordinateVector, representativeList[centroidIndices[k]].coordinateVector)
            
            # if this sum of distances is the biggest so far, update maxes
            if sumOfSquaredDist > maxDist and j not in centroidIndices:
                maxDist = sumOfSquaredDist
                maxInd = j
        centroidIndices.append(maxInd)

    centroids = []

    # make centroid coordinate vectors
    for centroidIndex in centroidIndices:
        centroids.append([coord for coord in representativeList[centroidIndex].coordinateVector])

    return (centroidIndices,centroids)


def findAverageInGroup(repGroup):
    """
    takes a group of representatives and finds the average of 
    their coordinateVectors, effectively finding the center of the
    group.
    """
    centroid = [0 for i in range(len(repGroup[0].coordinateVector))]

    # find the sum of all the vectors
    for rep in repGroup:
        centroid = list(map(add, centroid, rep.coordinateVector)) # i love haskell

    # divide sum by length of group
    centroid = list(map(lambda x : x / len(repGroup), centroid))
    return centroid


def kMeansIteration(centroids, representativeList):
    """
    run one iteration of k means, returning the newCentroids and
    their respective groups of representatives.
    """
    centroidGroups = [[] for i in range(len(centroids))]
    for rep in representativeList:
        centroid = -1
        minDist = float('inf')
        for i in range(len(centroids)):
            dist = getSquaredDistance(rep.coordinateVector, centroids[i])
            if dist < minDist:
                centroid = i
                minDist = dist
        centroidGroups[centroid].append(rep)

    newCentroids = []
    for centroidGroup in centroidGroups:
        newCentroids.append(findAverageInGroup(centroidGroup))

    return newCentroids, centroidGroups

def runKMeans(representativeList, numGroups):
    """
    runs the k-means algorithm. first, finds the initial centroids
    based on the representativeList and the desired number of 
    groups and then runs kMeansIteration() until no changes are
    made to the centroids.
    """
    centroidIndices, centroids = makeInitialCentroids(representativeList, numGroups)
    print("Initial centroids based on:  ", end='')
    for i in range(len(centroidIndices)-1):
        print(f"{representativeList[centroidIndices[i]].id}, ", end='')
    print(f"{representativeList[centroidIndices[len(centroidIndices)-1]].id}")
    rounds = 0
    running = True
    while running:
        newCentroids, centroidGroups = kMeansIteration(centroids, representativeList)
        rounds -=- 1 # one more time for old time's sake
        if centroids == newCentroids:
            rounds -= 1 # decrement since we did an extra round that did nothing
            running = False
        centroids = newCentroids

    print(f"Converged after {rounds} rounds of k-means.")
    for i in range(len(centroids)):
        # calculate the percentages of democrats and republicans in each group
        demAmt = len(list(filter(lambda rep : rep.party == 'D', centroidGroups[i])))/len(centroidGroups[i])*100
        repAmt = len(list(filter(lambda rep : rep.party == 'R', centroidGroups[i])))/len(centroidGroups[i])*100

        # print out group information
        print(f"    Group {i}:  size {len(centroidGroups[i])} ({demAmt:.3f}% D, {repAmt:.3f}% R)")

if __name__ == "__main__":
    # check that user is not trying to break the program
    if len(sys.argv) != 3:
        print("Incorrect Usage! Please provide a voting-data file and a number of centroids.")
        sys.exit(9)
    if int(sys.argv[2]) < 2:
        print("You must have at least two centroids.")
        sys.exit(9)

    # run k-means with appropriate arguments
    reps = readData(sys.argv[1])
    representativeList = makeRepresentativeList(reps)
    runKMeans(representativeList, int(sys.argv[2]))