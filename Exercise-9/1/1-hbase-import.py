import happybase
import re

N = 3

# establish connection to HBase database
conn = happybase.Connection(table_prefix='Fabian_Hoti')

# create table
conn.create_table(
        'articles', # the name of the table will be: 'Fabian_Hoti_articles'
        {'w':dict()}       # only one column family
)

table = conn.table('articles')

fd = open("/home/bigdata/9/enwiki-clean-10MiB.csv", "r")
line_idx = 0
for line in fd:
  # the first N articles are imported into the database
  if line_idx == N:
    break
  line_idx = line_idx + 1
  splitted = line.split(",")
  title = splitted[2]
  # the text consists of all splits after the first 3
  text = ''
  for idx in range(3,len(splitted)):
    text = text+splitted[idx]
  # convert text to lower case
  text = text.lower()
  # get a list of all words
  list_of_words = re.compile('\w+').findall(text)
  # create a new row for this article, containing a counter for each word
  for word in list_of_words:
    # the counter of a word is incremented for each occurrence of the word
    table.counter_inc(title.encode('ascii'),('w:'+word).encode('ascii'))
