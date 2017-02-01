from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
import numpy as np
import csv, io, sys, re

# this function calculates the cosine similarity for two instances of SparseVector
def cosine_similarity(a, b):
  return np.dot(a,b)/(np.sqrt(np.dot(a,a))*np.sqrt(np.dot(b,b)))

# create sparkContext
conf = SparkConf()
conf.setAppName("testFabian")
sc = SparkContext(conf=conf)

# Load articles and quotes (one per line).
wiki = sc.textFile("/user/bigdata/wikipedia-text-tiny-clean500").sample(False,0.001,42)
imdb = sc.textFile("imdb-quotes.csv").sample(False,0.01,42)

# we will work with relative word frequencies instead of absolut word counts, because otherwise
# longer quotes will be naturally closer to the wikipedia articles

# each article is mapped onto the tuple of title and the array with realative word frequency over the whole article
hashingTF = HashingTF()
articles = wiki.map(lambda line: (line.split(",")[2], (hashingTF.transform(re.compile('\w+').findall(line.lower())).toArray()))) \
               .map(lambda line: (line[0], line[1]/line[1].sum()))

# sum of word vectors of all articles 
sumOfArticles = wiki.map(lambda line: hashingTF.transform(re.compile('\w+').findall(line.lower())).toArray()) \
                    .reduce(lambda a,b: a+b)
# create a vector containing the relative word frequency over all articles
relativeArticleWordCount = sumOfArticles/sumOfArticles.sum()

# the relative word frequency is substracted from the relative word frequency per article
# therefore, a positive entry in the article array represents now a word that occurs more often in
# the article, than it does in average over all articles (analog for negative entries)
articles = articles.map(lambda line: (line[0], line[1]-relativeArticleWordCount))

# doing this substraction the array now contains a value for each word that measures 
# how typical this word is for the article

# the same processing is now done for quotes

# each quote is mapped onto a tuple of the quote self and the relative word frequency of the quote
quotes = imdb.map(lambda line: (line, hashingTF.transform(re.compile('\w+').findall(line.split('|')[4].lower())).toArray())) \
             .map(lambda line: (line[0], line[1]/line[1].sum()))

sumOfQuotes = imdb.map(lambda line: hashingTF.transform(re.compile('\w+').findall(line.split('|')[4].lower())).toArray()) \
                  .reduce(lambda a,b: a+b)
relativeQuoteWordCount = sumOfQuotes/sumOfQuotes.sum()
quotes = quotes.map(lambda line: (line[0], line[1]-relativeQuoteWordCount))

def findMax(a,b):
  if a[1] > b[1]:
    return a
  else:
    return b

# compare the normalized relative word frequencies of each article with each quote
# then return the quote with highest similarity
articleQuotes = articles.cartesian(quotes) \
                  .map(lambda line: (line[0][0], (line[1][0], cosine_similarity(line[0][1],line[1][1])))) \
                  .reduceByKey(findMax)

articleQuotes.take(20)

