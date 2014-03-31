import codecs

splitReviews = dict()

def isReviewRelevantToSynset(s):
    return lambda r: len(splitReviews[r['text']] & set(s)) != 0

def getSynsetReviews(s, reviews):
    return filter(isReviewRelevantToSynset(s), reviews)

def aggregateReviews(synsets, reviews):
    aggRevs = dict()
    for s in synsets:
        r = getSynsetReviews(s, reviews)
        if len(r) == 0:
            continue
        aggRevs[s] = getSynsetReviews(s, reviews)
        if verbose: print('\tSynset {}: {} reviews'.format(s, len(aggRevs[s])))
    return aggRevs

def loadObject(file):
    f = codecs.open(file, 'r', encoding = 'utf-8-sig')
    obj = eval(f.read())
    f.close()
    return obj

if __name__ == '__main__':
    verbose = True

    if verbose: print('')
    if verbose: print('Loading reviews...')

    reviews = loadObject('../Data/ProcessedReviews.txt')

    for app in reviews:
        for r in reviews[app]:
            splitReviews[r['text']] = set(r['text'].split())
    
    if verbose: print('')
    if verbose: print('Loading synsets...')

    synsets = loadObject('../Data/Synsets.txt')

    categorizedReviews = dict()

    for app in reviews:
    
        if verbose: print('')
        if verbose: print('Aggregating reviews for {}...'.format(app))

        categorizedReviews[app] = aggregateReviews(synsets, reviews[app])

    f = codecs.open('../Data/SynsetAggregatedReviews.txt', 'w+', encoding = 'utf-8-sig')
    f.write(str(categorizedReviews))
    f.close()