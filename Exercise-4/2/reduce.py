#!/usr/bin/python3

import sys
import re
import csv

def reducer():
  # our dictionary
  counter = {}
  article_counter = {}
  prev_title = ''
  prev_id = 0
  wordcount = 0
  for line in sys.stdin:
    (article_id,title,wordandcount) = line.split(';')
    (word,count) = wordandcount.split(',')
    if line == '':
      break;
    if prev_title == '':
      prev_title = title
      prev_id = article_id
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

  # für den letzten Artikel muss die Ausgabe noch stattfinden 
  print(prev_id,", ",prev_title,", ",wordcount,", ",article_counter,sep='')
  
  out = open('wiki-clean-frequency.csv', 'w')
  cout = csv.writer(out) 

  for word, count in counter.items():
    cout.writerow([word,count])


if __name__ == '__main__':
  reducer()
