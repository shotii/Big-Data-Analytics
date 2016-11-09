#!/usr/bin/python3

import psycopg2
import sys
import json
import itertools
import re
from timeit import default_timer as timer

# for the importer use
def parseCSV(conn, cursor):
  # only the first 3 articles are used
  number_of_articles = 3
  fd = open("/home/bigdata/3/enwiki-all-clean.csv", "r")
  for line in fd:
    splitted = line.split(",")
    text = ''
    # the text consists of all splits after the first 3
    for idx in range(3,len(splitted)):
      text = text+splitted[idx]
    if number_of_articles > 0:  
      cursor.execute("INSERT into articles VALUES(%s,%s,%s)", (splitted[0], splitted[2], text))
      conn.commit()
      number_of_articles = number_of_articles - 1


def main():
  # connect to the database
  conn = psycopg2.connect('user=schmid2 dbname=schmid2')

  # conn.cursor() returns a cursor object which allows to execute SQL queries
  cursor = conn.cursor()
  start = timer()
  parseCSV(conn,cursor)
  end = timer()
  print(end-start)

if __name__ == "__main__":
  main()
