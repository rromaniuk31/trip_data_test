# Trip Data Test 

## Introduction
In this repo you will find my work for the Senior Data Science Developer competition. This includes raw data which was ingested by the main.py python script, where a function was defined to update the duration fields to be in seconds. This newly updated data was then output to a parquet file for use by the business for self serve analytics. Accompanying these files is also the test_seconds.py file that uses pytest to check that the function defined in main.py correctly converts the durations to seconds.

## Conversion To Seconds Function
While exploring the data I noticed that the duration fields were not strictly hh:mm:ss and in fact could include days and be in the form d.hh:mm:ss. This caused an error while trying to convert the column to seconds since durations came in different formats.

To solve this problem I checked if a "." occured near the beginning of time duration, which indicated that the time was greater than 24 hours and formatted differently. I determined that the only values for the day part in the dataset were 1 and 2, so I added some code to multiply the number of days by 24 and add it to the hours. Doing this ensured that the data in each duration column contained consistent formatting and could be converted to seconds.

## Assumptions
1. All speed and distance measures are in KM
2. 

## Future Improvements
Instead of just having cases to check whether the duration field contains a day value of 0, 1 or 2, it would be ideal to write it such that future durations with day greater than two can be accounted for properly.
