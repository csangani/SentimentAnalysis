import json
import os
import unicodedata
import codecs
import re
import sys
import string
import collections
import math
import copy
import pickle
import Emoticons

reviewRepoBase = """M:\SkyDrive\Documents\Academics\IV\CS 221\Project\ReviewRepo"""

reviews = dict()

dataSet = []

bigramFeatures = False

verbose = False

learningRate = 0.0001

epsilon = 0.001

def hypothesis(weights, features):
    return 1/(1+math.exp(-svp(weights, features)))

def extractFeatures():
    # Extract Unigram Features
    for r in dataSet:
        r['features'] = collections.Counter(r['text'].split())

    if bigramFeatures:
        # Extract Bigram Features
        for r in dataSet:
            tokens = r['text'].split()
            numTokens = len(tokens)
            for i in range(numTokens - 1):
                bigramFeature = tokens[i] + ' ' + tokens[i + 1]
                r['features'].update({bigramFeature: 1})

    if featurePresence:
        for r in dataSet:
            for f in r['features']:
                r['features'][f] = 1 if r['features'][f] != 0 else 0


def svp(w1, w2):
    if len(w1) < len(w2):
        return sum([w1[x]*w2[x] for x in w1 if x in w2])
    else:
        return sum([w1[x]*w2[x] for x in w2 if x in w1])

def loadReviewsFromFiles():
    for file in os.listdir(reviewRepoBase):
        if verbose: print("Loading reviews from", file)
        with open(reviewRepoBase + "/" + file, encoding="utf_8_sig") as f:
            reviews[file] = json.load(f)
    if verbose: print("Reviews loaded.")
    if verbose: print("")

def pickReviewDataSet():
    print("Choose reviews to analyze:")
    print("")
    for i in range(len(reviews)):
        print("(" + str(i) + ")", list(reviews.keys())[i])
    print("(" + str(len(reviews)) + ")", "all")
    print("")
    inp = input("Choose option (default: " + str(len(reviews)) + "): ")
    option = len(reviews)
    try:
        if len(inp) > 0:
            option = int(inp)
            if option > len(reviews) or option < 0:
                raise Exception()
    except:
        print("")
        print("ERROR: Please select a valid option")
        print("")
        return pickReviewDataSet()
    return option

def loadDataSet(option):
    aggregatedReviews = []
    if option == len(reviews):
        for i in range(len(reviews)):
            aggregatedReviews.extend(reviews[list(reviews.keys())[i]])
    else:
        aggregatedReviews.extend(reviews[list(reviews.keys())[option]])
    aggregatedReviews = map(removeAuthorName, aggregatedReviews)
    aggregatedReviews = map(cleanReviewText, aggregatedReviews)

    dataSet.extend(aggregatedReviews)

def removeAuthorName(r):
    del r['authorName']
    return r

def cleanReviewText(r):
    review = r['text']
    
    # Convert to lowercase
    review = review.lower()

    # Replace emoticons
    review = Emoticons.replace(review)

    # Replace exclamation marks
    review = re.sub('!+', ' EXCLAMATION ', review)

    # Replace apostrophes
    review = re.sub('[\']+', '', review)

    # Replace punctuation
    review = re.sub('[' + string.punctuation + ']+', ' ', review)

    # Normalize whitespace
    review = re.sub('[' + string.whitespace + ']+', ' ', review)

    # Normalize rating
    r['rating'] = float(r['rating'] - 1)/4

    r['text'] = review
    return r

def learnWeights(trainSize, iters):

    weights = collections.defaultdict(float)

    trainSet = dataSet[:int(trainSize*len(dataSet))]
    testSet = dataSet[int(trainSize*len(dataSet)):]

    if verbose: print("Training set size:", len(trainSet))
    if verbose: print("Test set size:", len(testSet))
    if verbose: print("")

    prev_error = float('inf')

    i = 1

    # Learn weights
    while True:
        if verbose: print("Pass", i)
        i = i + 1
        count = 1
        
        newWeights = collections.defaultdict(float)
        newWeights.update(weights)

        # Stochastic Gradient Descent
        for r in trainSet:
            if verbose: sys.stdout.write("\r%i reviews processed" % count)
            if verbose: sys.stdout.flush()
            count = count + 1
            features = r['features']
            rating = r['rating']

            for f in features:
                newWeights[f] = newWeights[f] + learningRate * (rating - hypothesis(features, weights)) * features[f]
        
            weights.update(newWeights)

        # Compute Training Error
        error = 0
        for r in trainSet:
            features = r['features']
            rating = r['rating']
            error = error + (rating - hypothesis(features, weights)) ** 2
            
        error = error / len(trainSet)

        print("")
        print ("Training set error:", error)

        # Compute Test Error
        error = 0
        for r in testSet:
            features = r['features']
            rating = r['rating']
            error = error + (rating - hypothesis(features, weights)) ** 2
            
        error = error / len(testSet)

        print ("Test set error:", error)
        print("")

        if abs(error - prev_error) < epsilon:
            break

        prev_error = error

    return weights

if __name__ == '__main__':

    # Set Switches
    verbose = True
    bigramFeatures = True
    featurePresence = True

    loadReviewsFromFiles()

    option = pickReviewDataSet()

    if verbose: print("")
    if verbose: print("Processing data...")

    loadDataSet(option)

    if verbose: print("")
    if verbose: print("Extracting features...")
    
    extractFeatures()

    if verbose: print("")
    if verbose: print("Learning weights...")
    if verbose: print("")

    weights = learnWeights(0.9, 10)

    f = codecs.open('output.txt', 'w+', 'utf-8-sig')
    f.write(str(weights))
    f.close()
    
    print(list(reversed(sorted(weights, key=lambda x: weights[x])))[:20])
    print(sorted(weights, key=lambda x: weights[x])[:20])