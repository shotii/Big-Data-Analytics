#!/usr/bin/python3

import sys
import re
from nltk.stem.snowball import SnowballStemmer

def mapper():
  stemmer = SnowballStemmer("english")
  
  for line in sys.stdin:
    line = line.rstrip()
    splitted = line.split(",")
    text = ''
    # the text consists of all splits after the first 3
    for idx in range(3,len(splitted)):
      text = text+splitted[idx]
    text = re.sub(r'[^a-zA-Z\-\s]','',text)
    text = text.split(" ")
    for word in text:
      word = word.strip()
      if word != '':
        word = stemmer.stem(word)    
        # the key consists of article id, article title and the word seperated with a semicolon  
        print(splitted[0],";",splitted[2],";",word,",",1,sep = '')


if __name__ == '__main__':
  mapper()


