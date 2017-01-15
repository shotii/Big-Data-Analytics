#!/usr/bin/env python3

import csv

class dataflow:
  def __init__(self, dic = {}):
    # all tuples are saved as a dictionary
    self.dic = dic

  @staticmethod
  def read(fileName, char = ','):
    tuples = []
    with open(fileName, 'r') as csvFile:
      data = csv.reader(csvFile, delimiter = char)
      for row in data:
        tuples.append(tuple(row))
    dic = {}
    # without grouping all tuples are put in the group 'None'
    dic[None] = tuples
    return dataflow(dic)

  def write(self, fileName, char = ','):
    with open(fileName, 'w', newline='') as csvFile:
      data = csv.writer(csvFile, delimiter = char)
      for key in self.dic:
        data.writerows(self.dic[key])
      
  def filter(self, f):
    dic = {}
    for key in self.dic:
      tuples = []
      for t in self.dic[key]:
        if f(t):
          tuples.append(t)
      dic[key] = tuples
    return dataflow(dic)
    
  def map(self, f):
    dic = {}
    for key in self.dic:
      tuples = []
      for t in self.dic[key]:
        tuples.append(f(t))
      dic[key] = tuples
    return dataflow(dic)
    
  def flatmap(self, f):
    dic = {}
    for key in self.dic:        # per group
      tuples = []
      for t in self.dic[key]:   # per tuple in group
        tmp = []
        for c in t:             # per entry in tuple
          tmp2 = []
          splitted = f(c)
          for s in splitted:    # per value of tuple-entry
            if tmp != []:
              for t2 in tmp:    # per already computed tuple
                t3 = list(t2)
                t3.append(s)
                tmp2.append(t3)
            else:
              # create a new list if none exist
              tmp2.append([s])
          tmp = tmp2
        for newT in tmp:
          # convert lists to tuples and append them to the overall list of tuples
          tuples.append(tuple(newT))
      dic[key] = tuples
    return dataflow(dic)
    
  def group(self, f):
    dic = {}
    for key in self.dic:
      for t in self.dic[key]:
        if f(t) not in dic:
          # create a new list of tuples for this group
          dic[f(t)] = []
          # append tuple to the already existing list of tuples
        dic[f(t)].append(t)
    return dataflow(dic)
    
  def reduce(self, f):
    dic = {}
    for key in self.dic:
      # function is called for each group
      dic[key] = f(self.dic[key])
    return dataflow(dic)
      
  def join(self, y, f):
    tuples = []
    for key1 in self.dic:
      for t1 in self.dic[key1]:
        for key2 in y.dic:
          for t2 in y.dic[key2]:
            if f(t1, t2):
              tuples.append(t1 + t2)
    dic = {}
    dic[None] = tuples
    return dataflow(dic)
      
  def __str__(self):
    return str(self.dic)

if __name__ == "__main__":
  s = dataflow.read("stud.csv")
  # 22,"Fritz","Musterman",false
  # 23,"Nina","Musterfrau",true
  
  print(s)
  # without grouping all tuples are in the group 'None'
  # {None: [('22', 'Fritz', 'Musterman', 'false'), ('23', 'Nina', 'Musterfrau', 'true')]}

  # map tuples to only the first two entries, then filter to get the tuples with second entry "Fritz"
  bs = s.map(lambda x: (x[0], x[1])).filter(lambda x: x[1] == "Fritz")
  print(bs)
  # {None: [('22', 'Fritz')]}
  
  bs.write("out.csv")
  # 22,Fritz
  
  l = dataflow.read("lecture.csv",';')
  # 1;"Big Data";22,23
  # 2;"Hochleistungsrechnen";22
  
  print(l)
  #{None: [('1', 'Big Data', '22,23'), ('2', 'Hochleistungsrechnen', '22')]}

  # flatten all tuples by creating one tuple per comma seperated value
  l = l.flatmap(lambda x: x.split(','))
  print(l)
  # {None: [('1', 'Big Data', '22'), ('1', 'Big Data', '23'), ('2', 'Hochleistungsrechnen', '22')]}
  
  # group tuples by the second tuple entry
  lgrouped = l.group(lambda x: x[1])
  print(lgrouped)
  # {'Big Data': [('1', 'Big Data', '22'), ('1', 'Big Data', '23')], 'Hochleistungsrechnen': [('2', 'Hochleistungsrechnen', '22')]}
  
  # reduce each group to one value by summing the first tuple entry 
  print(lgrouped.reduce(lambda x: sum([int(y[0]) for y in x])))
  # {'Big Data': 2, 'Hochleistungsrechnen': 2}
  
  s = dataflow.read("stud.csv")
  l = dataflow.read("lecture.csv",';').flatmap(lambda x: x.split(','))
  # join students and lectures by matrikel
  j = s.join(l, lambda x, y: x[0] == y[2]) 
  print(j)
  # {None: [('22', 'Fritz', 'Musterman', 'false', '1', 'Big Data', '22'), ('22', 'Fritz', 'Musterman', 'false', '2', 'Hochleistungsrechnen', '22'), ('23', 'Nina', 'Musterfrau', 'true', '1', 'Big Data', '23')]}
  
  
