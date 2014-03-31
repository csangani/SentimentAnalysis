import os, pickle, codecs, random, sys
from collections import *

from nltk.corpus import wordnet as wn

def computeSSet(words):
    s = set()
    for w in words:
        synsets = wn.synsets(w)
        s.update(synsets)
    return s

def collectSynsets(words):
    
    if verbose: print('')
    if verbose: print('Computing word synsets...')
    synsets = dict([(w, computeSSet([w])) for w in words if len(computeSSet([w])) > 0])
    
    if verbose: print('')
    if verbose: print('Collecting connected synsets...')

    passes = 1
    
    if verbose: print ""

    allSynsets = set.union(*synsets.values())

    synsetTopicMap = dict([(s,[]) for s in allSynsets])

    count = 0

    totalCount = len(allSynsets) * len(words)

    temp = 0

    for s in allSynsets:
        for w in words:
            count = count + 1
            temp2 = int(count * 100. / totalCount)
            if temp != temp2:
                temp = temp2
                sys.stdout.write('\r{}% done'.format(temp))
                sys.stdout.flush()
            if w in synsets and s in synsets[w]:
                synsetTopicMap[s] += [w]
                
    if verbose: print ""
    if verbose: print ""
    if verbose: print "Removing duplicates..."

    result = list(set([tuple(sorted(v)) for v in synsetTopicMap.values()]))

    flag = True
    i = 0
    while flag:

        flag = False
        while i < len(result):
            j = 0
            while j < len(result):
                if set(result[i]).issubset(set(result[j])) and set(result[i]) != set(result[j]):
                    flag = True
                    del result[i]
                    break
                elif set(result[j]).issubset(set(result[i])) and set(result[i]) != set(result[j]):
                    flag = True
                    del result[j]
                j = j + 1
            i = i + 1

    if [] in result: result.remove([])

    return result

def loadWeights(path):
    f = codecs.open(path, 'r', 'utf-8-sig')
    obj = eval(f.read())
    f.close()
    return obj

if __name__ == '__main__':
    verbose = True

    if verbose: print('Loading weights...')

    weights = loadWeights('../Data/FeatureWeights.txt')
    synsets = collectSynsets(weights.keys())

    if verbose: print ""

    f = codecs.open('../Data/Synsets.txt', 'w+', 'utf-8-sig')
    f.write(str(synsets))
    f.close()
    
      
