#!/usr/bin/python3

import psycopg2
import sys
import json
import itertools
import re
import csv
from timeit import default_timer as timer

def count_words(cursor):
  # get the count of each word for each article
  cursor.execute("SELECT id, word[1], count(*) FROM (SELECT regexp_matches(lower(a.text), '[A-Za-z\-]*', 'g') AS word, a.id FROM articles as a) AS view GROUP BY word, id ORDER BY word ASC")
  records = cursor.fetchall()

  out = open('output.csv', 'w')
  cout = csv.writer(out)
  
  for record in records:
    # article id, word and count is added as a row in the output.csv file
    cout.writerow([record[0], record[1], record[2]])


def main():
  # connect to the database
  conn = psycopg2.connect('user=schmid2 dbname=schmid2')

  # conn.cursor() returns a cursor object which allows to execute SQL queries
  cursor = conn.cursor()
  start = timer()
  count_words(cursor)
  end = timer()
  print(end-start)

if __name__ == "__main__":
  main()
