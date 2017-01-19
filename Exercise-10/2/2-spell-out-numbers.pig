fifa = LOAD '/user/bigdata/1998_FIFA_World_Cup' USING PigStorage() AS (txt:chararray);
Register '/home/hoti/numbers.py' USING jython as numbers;
fifa_new = FOREACH fifa GENERATE numbers.replace_numbers(1,100,txt);
STORE fifa_new INTO 'results/fifa.txt' USING PigStorage('\n');


