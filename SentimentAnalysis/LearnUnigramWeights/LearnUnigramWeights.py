import json
import os
import unicodedata
import codecs
import re
import sys
import string
import collections
import math
import Emoticons

reviews = dict()

dataSet = []

bigramFeatures = False
verbose = False
stochastic = False
stopWords = []

def hypothesis(weights, features):
    return 1/(1+math.exp(-svp(weights, features)))

def extractFeatures():
    # Extract Unigram Features
    for r in dataSet:
        r['features'] = collections.Counter(r['text'].split())

        for w in stopWords:
            if w in r['features']:
                del r['features'][w]

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

def loadStopWords():
    f = open('../Data/StopWords.txt', 'r')
    stopWords.extend([w.strip() for w in f.readlines()])
    f.close()

def loadReviewsFromFiles():
    f = codecs.open('../Data/ProcessedReviews.txt', 'r', encoding = 'utf-8-sig')
    reviews.update(eval(f.read()))
    f.close()

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

def learnWeights(trainSize, learningRate = 0.0001, epsilon = 0.001):

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
        if verbose: print ("Pass", i)
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
            
            if stochastic: weights.update(newWeights)

        if not stochastic: weights.update(newWeights)

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

    return dict(weights)

if __name__ == '__main__':

    # Set Switches
    verbose = True
    bigramFeatures = False
    featurePresence = True
    stochastic = False

    if verbose: print("")
    if verbose: print("Loading stop words...")

    loadStopWords()
    
    if verbose: print("")
    if verbose: print("Loading data...")

    loadReviewsFromFiles()

    option = pickReviewDataSet()
    
    if verbose: print("")
    if verbose: print("Aggregating data...")

    loadDataSet(option)

    if verbose: print("")
    if verbose: print("Extracting features...")
    
    extractFeatures()

    if verbose: print("")
    if verbose: print("Learning weights...")
    if verbose: print("")

    weights = learnWeights(0.9)

    f = codecs.open('../Data/FeatureWeights.txt', 'w+', 'utf-8-sig')
    f.write(str(weights))
    f.close()
    
    print(list(reversed(sorted(weights, key=lambda x: weights[x])))[:30])
    print(sorted(weights, key=lambda x: weights[x])[:30])