# Feature Based Opinion Extraction from Customer Reviews
As e-commerce and these online services are becoming more and more popular, the number of customer reviews that a product receives grows
rapidly which gives rise to the need to automating the process of reading the reviews and drawing meaningful summaries from the reviews which would help not only the customers to make decisions on whether to buy the product but also to the manufacturer to know exactly what all things need to be improved in the existing product and which ones to prioritize.
<br/><br/>
In this project, we implemented and extended some of the existing works on feature extraction and sentiment analysis for better and more informative summarizing. We firstly extract the one word features from a set of reviews based on their frequency of occurrence followed by association rules mining to get a list of two of word features by examining the words that occur frequently. This is followed by sentiment analysis of each and every feature to get an overall sentiment of a particular feature. We do not summarize the reviews by selecting or rewriting a subset of the original sentences from the reviews to capture their main points as in the classic text summarization. In this work, we only focus on mining opinion/product features that the reviewers have commented on.

## Approach
The following figure gives the architectural overview of our opinion extraction system. The
inputs to the system are the product reviews of all the customers. The output is
the summary of the reviews.
<p align="center">
  <img src="approach.png">
</p>
The system involves three main steps:
1. Review Cleaning
2. Mining the frequent product features that have been commented on
by the customers
3. Identify the customer opinions and the opinion intensities for
each product feature. <br/>
A detailed project report can be found [here](Project Report.pdf).

### 1. Review Cleaning
For the feature extraction part, we neglect any emojis and
demojify our review dataset before proceeding further. The minimum word length required is two for a review to be meaningful for our analysis.
We remove all the reviews of one word length, as they are mainly an adjective for the
whole product. We also remove any two word length review which does not contain
(noun+adjective) pair, hence shrinking our review corpus for analysis. All of the
review corpus is also turned to lowercase to avoid distinction between words like
’Camera’ and ’camera’ during POS tagging

### 2. Frequent Feature Identification
In our work, we will only mine for the frequent features. Features
can be explicitly or implicitly mentioned in a review. For example, ”The camera
is amazing but overall, it is not worth spending on the phone.” Here, ’camera’ is
an explicit feature whereas ’value of money’ is an implicit feature. We only extract
the explicit features as the implicit ones are difficult to mine. Human errors are
unavoidable. We have incorporated the spelling correction in our work which takes care of the
cases which have not more than one error in the spelling. So, words like ’camara’
are treated as ’camera’ but the words like ’cemara’ are not corrected. The following
NLP methods have been used for frequent features identification:
- POS tagging
- Association Rules mining
- Feature Pruning techniques
- Spelling correction using Levenshtein's distance <br/>
You can find detailed explanation of each in the [report](Project Report.pdf).

### 3. Opinion mining and sentiment scoring
Our first task is to mine the opinion words corresponding to the feature in the
sentence. We will focus on explicit opinions in our work as implicit opinions are difficult to
mine. In this work, we assume that a customer expresses a single opinion
about a particular feature in a sentence in his/her review, which is the usual case. We extract the nearest opinionated phrase to a feature.
Next, sentiment scores are obtained based on the intensity of emotions in
opinions. We use VADER (Valence Aware Dictionary and sEntiment Reasoning) for polarity extraction and scoring the sentiments. The
total positive and total negative polarity scores were taken to get the final sentiment
score of a particular feature as follows: <br/>
Sentiment Score = Total Positive Polarity / (Total Positive Polarity + Total Negative Polarity)


## Conclusion
In this project, we propose a pipeline to extract meaningful features from the
customer reviews and get a sentiment score for each feature which is a measure of
positive polarity towards that feature. To achieve this objective, we divide our
pipeline into three major sections - cleaning, feature extraction and opinion
mining. Cleaning the dataset involves cleaning the reviews and removing all
useless data. Feature extraction pipeline generates a list of meaningful features.
Finally, opinions towards features are extracted and sentiment scores are assigned
to each feature in the opinion mining pipiline. We have evaluated this method on a
review dataset of smartphone of a popular brand and the results were meaningful.
