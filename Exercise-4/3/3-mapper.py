#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')

    # As key we will use a concatenation of experiment names
    experimentsKey   = line[0] + line[1] + line[2] + line[3]
    experimentsValue = list()

    columnParts = line[4:len(line)]

    for value in columnParts:
        experimentsValue.append(float(value))

    # Separate key value by tab
    print("%s\t%s" % (experimentsKey, experimentsValue))