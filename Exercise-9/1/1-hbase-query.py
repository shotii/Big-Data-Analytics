# usage: python3 1-hbase-query.py "word"

import sys
import happybase

def query(word):
  # establish connection to HBase database
  conn = happybase.Connection(table_prefix='Fabian_Hoti')
  table = conn.table('articles')
  # iterate over all table rows
  for key, data in table.scan():
    # search for the word in the current row
    if table.row(key, columns = [('w:'+word).encode('ascii')]) != {}:
      print(key.decode('ascii'))


if __name__ == "__main__":
    query(sys.argv[1])
