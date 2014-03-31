import os, pickle, codecs, random, sys
from collections import *

verbose = True

def index_min(values):
    return min(range(len(values)), key=values.__getitem__)

def clusterWeights(weights, numClusters):
    assignments = dict([(w, -1) for w in weights])

    clusters = []

    for i in range(numClusters):
        clusters.append(random.random())

    flag = True
    
    i = 1

    while flag:
        if verbose: print("")
        if verbose: print "Pass", i
        i = i + 1
        count = 1
        flag = False
        
        if verbose: print("")
        if verbose: print ("Stage 1: Assigning clusters")
        for w in weights:
            if verbose: sys.stdout.write("\r%i words processed" % count)
            count = count + 1
            distances = [abs(c-weights[w]) for c in clusters]
            minIndex = index_min(distances)
            if assignments[w] != minIndex:
                flag = True
            assignments[w] = minIndex

        clusters = [0]*numClusters
        nums = [1]*numClusters

        if verbose: print("")
        
        count = 1
        
        if verbose: print("")
        if verbose: print ("Stage 2: Computing centroids")

        for a in assignments:
            if verbose: sys.stdout.write("\r%i words processed" % count)
            count = count + 1
            clusters[assignments[a]] += weights[a]
            nums[assignments[a]] += 1
            
        if verbose: print("")

        for s in range(len(clusters)):
            clusters[s] /= nums[s]
            
    if verbose: print("")
    if verbose: print("Saving results")

    result = [[] for s in range(numClusters)]
    for a in assignments:
        result[assignments[a]] += [a]

    return (result, clusters)


def loadWeights(path):
    f = codecs.open(path, 'r', 'utf-8-sig')
    obj = eval(f.read())
    f.close()
    return obj

if __name__ == '__main__':
    if verbose: print('Loading weights...')

    weights = loadWeights('../Data/FeatureWeights.txt')
    
    result, clusters = clusterWeights(weights, 3)

    f = codecs.open('../Data/FeatureClusters.txt', 'w+', 'utf-8-sig')
    f.write(str(clusters))
    f.close()

    positiveWords = result[clusters.index(max(clusters))]
    negativeWords = result[clusters.index(min(clusters))]

    subjectiveWords = positiveWords + negativeWords

    newWeights = dict()
    newWeights.update(weights)

    for w in weights:
        if w not in subjectiveWords:
            del newWeights[w]

    f = codecs.open('../Data/FilteredFeatureWeights.txt', 'w+', 'utf-8-sig')
    f.write(str(newWeights))
    f.close()