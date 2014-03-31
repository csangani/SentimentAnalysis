*******************************************************************************
*	Sentiment Analysis
*******************************************************************************

Author:	Chirag Sangani
	csangani@stanford.edu

	Sundaram Ananthanarayanan
	sananth2@stanford.edu

-------------------------------------------------------------------------------
-	README
-------------------------------------------------------------------------------

The code is divided into two parts: data aggregation and sentiment analysis.

1. Data Aggregation:
	Netbeans project under "AndroidCommentScraper" for Java.
	To set up, insert your gmail ID / password in SessionSetup.java

	App ID scraper helps in determining app IDs. This app ID can then be
	used to scrape comments using CommentsScraper.

2. Sentiment Analysis
	Visual Studio solution under "SentimentAnalysis" for Python. Use
	PyTools plugin for Visual Studio. The solution contains the following
	projects in order of usage:

	a. ReviewCleaner
	Python 3.3
	Process reviews for usage.

	b. LearnUnigramWeights
	Python 3.3
	Run regression on features

	c. CollectSynsets
	Python 2.7. Needs NLTK.
	Collect words into synset topics

	d. SynsetReviewAggregator
	Python 2.7
	Aggregate reviews under topics

	e. ComputeSynsetMetrics
	Python 2.7
	Compute metrics for each topic.

	All data is present in the "/SentimentAnalysis/Data" folder.

	Except for the NLTK code that provided synsets for a single word, all
	code, including regression, clustering, and ranking was written by us.