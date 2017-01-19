data = LOAD '/home/bigdata/10-numbers' USING PigStorage() AS (nr:int);
grouped = group data all;
mavg = foreach grouped generate AVG(data.nr);
DUMP mavg;

Result: (16417.518324816752)
