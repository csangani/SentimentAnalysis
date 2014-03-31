import codecs, collections

weights = []

def computeSynsetMetrics(reviews, synset):
    synsetMetrics = dict()
    sortedRatings = sorted([r['rating'] for r in reviews])
    synsetMetrics['ratingAverage'] = sum(sortedRatings) / len(sortedRatings)
    synsetMetrics['ratingMedian'] = (sortedRatings[len(sortedRatings)/2] if len(sortedRatings) % 2 != 1 else (sortedRatings[len(sortedRatings)/2] + sortedRatings[len(sortedRatings)/2]) / 2) if len(sortedRatings) > 1 else sortedRatings[0]
    synsetMetrics['numReviews'] = len(reviews)
    synsetMetrics['averageWeight'] = sum([weights[w] for w in synset]) / len(synset)
    synsetMetrics['minWeight'] = min([weights[w] for w in synset])
    synsetMetrics['maxWeight'] = max([weights[w] for w in synset])
    synsetMetrics['reviews'] = reviews
    return synsetMetrics

def computeAppMetrics(reviews):
    appMetrics = dict()
    for synset in reviews:
        if verbose: print('\tSynset {}'.format(synset))
        appMetrics[synset] = computeSynsetMetrics(reviews[synset], synset)
    return appMetrics

def computeMetrics(aggReviews):
    metrics = dict()
    for app in aggReviews:

        if verbose: print('')
        if verbose: print('Computing metrics for {}...'.format(app))

        metrics[app] = computeAppMetrics(aggReviews[app])
    return metrics

def loadObject(file):
    f = codecs.open(file, 'r', encoding = 'utf-8-sig')
    obj = eval(f.read())
    f.close()
    return obj

if __name__ == '__main__':
    verbose = True

    if verbose: print('')
    if verbose: print('Loading weights...')

    weights = loadObject('../Data/FeatureWeights.txt')

    if verbose: print('')
    if verbose: print('Loading synset-aggregated reviews...')

    aggRevs = loadObject('../Data/SynsetAggregatedReviews.txt')

    if verbose: print('')
    if verbose: print('Loading reviews...')

    reviews = loadObject('../Data/ProcessedReviews.txt')

    metrics = computeMetrics(aggRevs)

    f = codecs.open('../Data/SynsetMetrics.txt', 'w+', encoding = 'utf-8-sig')
    #f.write(str(metrics))
    f.close()

    f = codecs.open('../Data/FinalOutput.txt', 'w+', encoding = 'utf-8-sig')

    for app in metrics:
        f.write("Secret Sauce metrics for {}:".format(app) + '\r\n')
        avgR = sum([r['rating'] for r in reviews[app]])/len(reviews[app])
        f.write("Average rating: {}".format(avgR) + '\r\n')
        synsets = filter(lambda x: metrics[app][x]['numReviews'] > 10, metrics[app].keys())
        synsets = sorted(synsets, key=lambda x: -((metrics[app][x]['ratingAverage']-avgR)**2)*(metrics[app][x]['ratingAverage']**2)*(1-metrics[app][x]['ratingAverage'])**2*metrics[app][x]['numReviews'])[:10]
        for s in synsets:
            f.write(str(s) + '\r\n')
            rating = metrics[app][s]['ratingAverage']
            rvs = sorted(metrics[app][s]['reviews'], key=lambda x: ((x['rating'] - rating) ** 2) / (sum([collections.Counter(x['text'].split())[w] for w in collections.Counter(x['text'].split()) if w in s]) + 1))[:4]
            for r in rvs:
                f.write('\t\t')
                f.write(repr(r['text']))
                f.write('\r\n')
            f.write('\t{} reviews, {} avg, {} min, {} max'.format(metrics[app][s]['numReviews'], metrics[app][s]['ratingAverage'], metrics[app][s]['minWeight'], metrics[app][s]['maxWeight']) + '\r\n')
            
    for app in metrics:
        f.write("Positive metrics for {}:".format(app) + '\r\n')
        avgR = sum([r['rating'] for r in reviews[app]])/len(reviews[app])
        f.write("Average rating: {}".format(avgR) + '\r\n')
        synsets = filter(lambda x: metrics[app][x]['numReviews'] > 10, metrics[app].keys())
        synsets = sorted(synsets, key=lambda x: -metrics[app][x]['averageWeight'] - metrics[app][x]['ratingAverage'])[:10]
        for s in synsets:
            f.write(str(s) + '\r\n')
            rating = metrics[app][s]['ratingAverage']
            rvs = sorted(metrics[app][s]['reviews'], key=lambda x: ((x['rating'] - rating) ** 2) / (sum([collections.Counter(x['text'].split())[w] for w in collections.Counter(x['text'].split()) if w in s]) + 1))[:4]
            for r in rvs:
                f.write('\t\t')
                f.write(repr(r['text']))
                f.write('\r\n')
            f.write('\t{} reviews, {} avg, {} min, {} max'.format(metrics[app][s]['numReviews'], metrics[app][s]['ratingAverage'], metrics[app][s]['minWeight'], metrics[app][s]['maxWeight']) + '\r\n')

    for app in metrics:
        f.write("Negative metrics for {}:".format(app) + '\r\n')
        avgR = sum([r['rating'] for r in reviews[app]])/len(reviews[app])
        f.write("Average rating: {}".format(avgR) + '\r\n')
        synsets = filter(lambda x: metrics[app][x]['numReviews'] > 10, metrics[app].keys())
        synsets = sorted(synsets, key=lambda x: metrics[app][x]['averageWeight'] + metrics[app][x]['ratingAverage'])[:10]
        for s in synsets:
            f.write(str(s) + '\r\n')
            rating = metrics[app][s]['ratingAverage']
            rvs = sorted(metrics[app][s]['reviews'], key=lambda x: ((x['rating'] - rating) ** 2) / (sum([collections.Counter(x['text'].split())[w] for w in collections.Counter(x['text'].split()) if w in s]) + 1))[:4]
            for r in rvs:
                f.write('\t\t')
                f.write(repr(r['text']))
                f.write('\r\n')
            f.write('\t{} reviews, {} avg, {} min, {} max'.format(metrics[app][s]['numReviews'], metrics[app][s]['ratingAverage'], metrics[app][s]['minWeight'], metrics[app][s]['maxWeight']) + '\r\n')

    f.close()