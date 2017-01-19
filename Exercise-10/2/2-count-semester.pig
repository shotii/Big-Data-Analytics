semesters = LOAD '/home/bigdata/10-semesters' USING PigStorage(',') AS (studId:int, year:int);
filterered_sem = FILTER semesters BY studId >= 0;

students = LOAD '/home/bigdata/10-numbers' USING PigStorage(,) AS (studName:chararray, studId:int);
filtered_stud = FILTER students BY studId >= 0;

stud_sem = JOIN filtered_stud by studId, filtered_sem by studId;
stud_sem2 = GROUP by studName;

DUMP stud_sem2;

