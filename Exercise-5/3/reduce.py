#!/usr/bin/python3

import sys
import re


def reducer():
  last_netcdf = []
  waitlist = []
  for line in sys.stdin:   
    line = line.rstrip()
    line = line.split(";")    
    if len(line) == 5:    # netcdf.csv line
      if last_netcdf == []: # once the first netcdf.csv line appears all deferred wiki-coordinates.csv lines have to be processed 
        for wiki_line in waitlist:
          print(wiki_line[3],", (",wiki_line[1]," : ",wiki_line[2],"), ",line[4],", ",line[3], sep='')
      last_netcdf = line  
    elif len(line) == 4:  # wiki-coordinates.csv line
      if last_netcdf == []: # if no netcdf.csv line has appeared yet this line has to be processed later
        waitlist.append(line)
      else: # it is estimated that the place from the wiki-coordinates.csv line is near the place from the last netcdf.csv line 
        print(line[3],", (",line[1]," : ",line[2],"), ",last_netcdf[4],", ",last_netcdf[3], sep='')
    else:
      print(line)
      print("Error")
      break


if __name__ == '__main__':
  reducer()
