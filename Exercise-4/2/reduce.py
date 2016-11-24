#!/usr/bin/python3

import sys
import re
import csv

def reducer():
  # dictionary that counts word occurances over all articles
  counter = {}
  # dictionary that counts word occurances over the current article
  article_counter = {}
  prev_title = ''
  prev_id = 0
  wordcount = 0
  for line in sys.stdin:
    (article_id,title,wordandcount) = line.split(';')
    (word,count) = wordandcount.split(',')
    # have we reached the end of the input?
    if line == '':
      break;
    # processing the special case of the first article
    if prev_title == '':
      prev_title = title
      prev_id = article_id
    # if prev_title != title we completed the previous article
    if prev_title != title:  
      print(prev_id,", ",prev_title,", ",wordcount,", ",article_counter,sep='')
      prev_title = title
      prev_id = article_id
      wordcount = 0
    wordcount = wordcount + 1
    word = word.strip()
    if word in article_counter:
      article_counter[word] = article_counter[word] + int(count)
    else:
      article_counter[word] = int(count)
    if word in counter:
      counter[word] = counter[word] + int(count)
    else:
      counter[word] = int(count)

  # output for the last article has to be done 
  print(prev_id,", ",prev_title,", ",wordcount,", ",article_counter,sep='')
  
  out = open('wiki-clean-frequency.csv', 'w')
  cout = csv.writer(out) 

  for word, count in counter.items():
    cout.writerow([word,count])


if __name__ == '__main__':
  reducer()
