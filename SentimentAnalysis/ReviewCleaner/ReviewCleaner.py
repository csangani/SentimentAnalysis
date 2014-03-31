import codecs, os, json, Emoticons, re, string

def loadReviewsFromFiles(base):
    reviews = dict()
    for file in os.listdir(base):
        with codecs.open(base + "/" + file, 'r', encoding="utf_8_sig") as f:

            if verbose: print("")
            if verbose: print("Loading reviews for {}...".format(file))

            reviews[file] = json.load(f)
            reviews[file] = list(map(removeUnnecessaryData, reviews[file]))
            reviews[file] = list(map(cleanReviewText, reviews[file]))
    return reviews

def removeUnnecessaryData(r):
    del r['authorName']
    del r['creationTime']
    del r['authorId']
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

if __name__ == '__main__':
    verbose = True

    if verbose: print("")
    if verbose: print("Loading data...")

    dataSet = loadReviewsFromFiles('../Data/Reviews')

    f = codecs.open('../Data/ProcessedReviews.txt', 'w+', 'utf-8-sig')
    f.write(str(dataSet))
    f.close()