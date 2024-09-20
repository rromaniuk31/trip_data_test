# Trip Data Test 

## Introduction
In this repo you will find my work for the Senior Data Science Developer competition. This includes raw data which was ingested by the main.py python script, where a function was defined to update the duration fields to be in seconds. This newly updated data was then output to a parquet file for use by the business for self serve analytics. Accompanying these files is also the test_seconds.py file that uses pytest to check that the function defined in main.py correctly converts the durations to seconds.

## Conversion To Seconds Function
While exploring the data I noticed that the duration fields were not strictly hh:mm:ss and in fact could include days and be in the form d.hh:mm:ss. This caused an error while trying to convert the column to seconds since durations came in different formats.

To solve this problem I checked if a "." occured near the beginning of time duration, which indicated that the time was greater than 24 hours and formatted differently. I determined that the only lengths for the day part in the dataset were 1 and 2, so I added some code to multiply the number of days by 24 and add it to the hours. Doing this ensured that the data in each duration column contained consistent formatting and could be converted to seconds.

## Assumptions
1. I assumed that the only transformations that the business required was creating a new column for each of the duration fields that converts the fields into seconds. Since I don't have access to anyone from the business side to confirm I did not alter any of the other data to ensure that all potential applications that are downstream are not impacted by my changes. If the business were to require any other transformations we can talk about the implementation of those later, since I didn't want to alter the data in a way the business didn't expect.
2. I assume that the "engineHours" field has an issue with the recording of this data since 95% of it contains null values. Had the field been, for example 95% filled, I may have looked at different ways to impute the missing data and brought my idea to the business. But in the meantime the next time I spoke with the business I would bring this field to their attention to ensure the telematics device they are tracking this field with is in working order.
3. The "averageSpeed" column also contains 11 rows with null values, this occurs when "distance" is zero. In this case it would make the most sense to either impute zero for "averageSpeed" in these rows, but since these were trips of 0KM maybe the business would prefer if we just dropped these rows. I would have to get a better understanding for how the data will be used to decide which route to take, so for now I left them as null until I can meet with a subject matter expert.
4. All speed and distance measures are in KM.


## Future Improvements
1. Instead of just having cases to check whether the duration field contains a day value of length 0, 1 or 2, it would be ideal to write it such that future durations with day length greater than two can be accounted for properly.
2. In this case it's not an issue, since we don't have a big dataset, but it would likely be beneficial to update the for loop in our function that loops through the rows to something more compute efficient like a list comprehension.
