from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from operator import add
import re
import collections

WORD = 'computer'

# create sparkContext
conf = SparkConf()
conf.setAppName("testFabian")
sc = SparkContext(conf=conf)

def parseInput(file_name="/user/bigdata/wikipedia-text-tiny-clean500"):
  # Read in the data and clean it
  rdd = sc.textFile(file_name)
  return rdd

rdd = parseInput()

# split each line into words, flatMap into tuples of (article, word) and filter
words = rdd.map(lambda x: x.split(' ')).flatMap(lambda x: [(x[0], e) for e in x]) \
           .filter(lambda x: x[1] == WORD)

# multiple occurances per article shouldnt be counted
counts = words.groupByKey()
print("Absolut count of articles:",counts.count())
print("Relative count of articles:",float(counts.count())/rdd.count())

# articles containing the word
articles = rdd.filter(lambda x: WORD in x.split(' '))

# Each article is saved in a file in the folder 'output'
articles.saveAsTextFile('output')

# using accumulators
overall_count = sc.accumulator(0)
word_count = sc.accumulator(0)

def increment(article):
  overall_count.add(1)
  if WORD in article:
    word_count.add(1)

rdd.foreach(increment)
print("Absolut count: %s, relative count %f" % (word_count, float(word_count.value)/overall_count.value))

sqlContext = SQLContext(sc)

words = rdd.map(lambda x: x.split(' ')).flatMap(lambda x: [(x[0], e) for e in x])
df = sqlContext.createDataFrame(words, ["article","word"])
df.registerTempTable("articles")

res = sqlContext.sql("SELECT count(iCount) FROM (SELECT count(*) AS iCount FROM articles WHERE word=='computer' GROUP BY article) as Count where iCount > 0")
print(res.collect())
