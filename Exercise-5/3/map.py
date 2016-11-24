#!/usr/bin/python

from __future__ import print_function
import sys
import re
import struct

# this function calculates a binary representation of a float
def binary(num):
  return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', float(num)+1000))
  
# this function takes two binaries n1 and n2 (as strings) and builds a string conj = n1[0]+n2[0]+... 
def conjunct(n1,n2):
  conj = ''
  n1 = binary(n1)
  n2 = binary(n2)
  for i in range(len(n1)):
    conj = conj + n1[i] + n2[i]
  return conj
  

def mapper():
  for line in sys.stdin:
    line = line.rstrip()
    # quotes are around names of places from wiki-coordinates that contain commas
    search_quotes = re.match(r"(\".*\")(.*)", line)
    if search_quotes is not None:
      splitted = search_quotes.group(2).split(",")
      # the key is the conjunct of the coordinates
      # as value the coordinates as floats and the name of the place is printed
      print(conjunct(splitted[1],splitted[2]),",;",splitted[1],";",splitted[2],";",search_quotes.group(1),sep='') 
      continue
    splitted = line.split(",")
    # no quotes in wiki-coordinates.csv line
    if len(splitted) == 3:
      print(conjunct(splitted[1],splitted[2]),",;",splitted[1],";",splitted[2],";",splitted[0],sep='')    
    # a netcdf.csv line
    elif len(splitted) == 5:
      if splitted[0] != "date":
        # as value the coordinates as floats, the temperature and the precipitation are printed
        print(conjunct(splitted[1],splitted[2]),",;",splitted[1],";",splitted[2],";",splitted[3],";",splitted[4],sep='') 
        

if __name__ == '__main__':
  mapper()


