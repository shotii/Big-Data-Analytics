from itertools import zip_longest
import sys

current_experiment = None

# Initialize empty list with 260 zeros
current_values = [0.0] * 260

# Counter required for mean computation for each experiment later
experiments_counter = 1
experiment = None

# Input of the csv file given by hadoop streaming api through sys.stdin
for line in sys.stdin:
    # Get rid of any leading or trailing whitespace
    line = line.strip()

    # The input of mappter, i.e. key as experiment and list of values namely for each column 1 value in list
    (experiment, valuesAsStr) = line.split('\t')
    valuesAsStr = valuesAsStr.replace('[','')
    valuesAsStr = valuesAsStr.replace(']', '')
    values = valuesAsStr.split(',')

    # Since the map output is sorted by hadoop we expect the same key to show up subsequently
    if experiment == current_experiment:
        # The lists of the same experiments are added element wise together which corresponds to their
        # columns being added together, if one list is longer than the other fill the smaller one with zeros

        current_values = [float(x) + float(y) for x, y in zip_longest(current_values, values, fillvalue=0)]
        experiments_counter += 1
    else:
        if current_experiment:
            # Compute mean as required in task from all summed up values and the experiment counter then print to stdout
            mean_values = [x / experiments_counter for x in current_values]
            print('%s\t%s' % (current_experiment, mean_values))

        # Reinitialize values for next experiment
        current_experiment = experiment
        current_values = values
        experiments_counter = 1


# It may happen that the last experiment is not printed, so here it is ensured
if current_experiment == experiment:
    mean_values = [x / experiments_counter for x in current_values]
    print('%s\t%s' % (current_experiment, mean_values))



