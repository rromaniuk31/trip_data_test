# Import packages
import numpy as np
import pandas as pd
import pytest
import warnings
import datetime
import random
import fastparquet

# Set a random seed in case there is ever a requirement regarding reproducability
random.seed(2024)

# Suppress warnings 
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

# Get data
df = pd.read_json("trip_data.json")

# Define a function to convert durations to seconds
def convert_to_seconds(df, cols):
    '''This function takes a dataframe and a list of columns to be 
    converted to seconds and returns the dataframe with additional 
    columns that have been converted to seconds.
    '''       

    # Loop through the duration columns    
    for i in cols:
        # Create a temporary column for the updated format of the duration column
        temp_col = i + "_temp"
        df[temp_col] = -1
        # Loop through the rows in the dataframe
        for j in range(0, len(df[temp_col])):
            # Check if a "." occurs early in the duration, if so, the number before it is the day
            dec_loc = df[i][j].find(".", 0, 3)
            # Hours update if number of days is between 1 and 9 (inclusive)
            if dec_loc == 1:
                adj_hours = int(df[i][j][2:4]) + 24 * int(df[i][j][0:1])
                df[temp_col][j] = str(adj_hours) + df[i][j][4:]
            # Hours update if number of days is between 10 and 99 (inclusive)
            elif dec_loc == 2:
                adj_hours = int(df[i][j][3:5]) + 24 * int(df[i][j][0:2])
                df[temp_col][j] = str(adj_hours) + df[i][j][5:]
            # No update if no days value
            else:
                df[temp_col][j] = df[i][j]
        
        # Create seconds column
        new_sec_col = i + "_seconds"
        # Determine number of seconds in duration and put it in seconds column
        df[new_sec_col] = pd.to_timedelta(df[temp_col]).dt.total_seconds()
        
        # Drop the temporary column
        df = df.drop(temp_col, axis=1)
    return(df)

# Create a list of the duration columns and give this list and the dataframe to our function
cols = ["afterHoursDrivingDuration", "afterHoursStopDuration", "drivingDuration", "idlingDuration", "speedRange1Duration", "speedRange2Duration", "speedRange3Duration", "stopDuration", "workDrivingDuration", "workStopDuration"]
seconds_df = convert_to_seconds(df, cols)

# Save our functions output as a parquet file
seconds_df.to_parquet('trip_data_withSeconds.parquet')

# Print which columns have null values for future conversations with the business
all_cols = list(df.columns)
for i in all_cols:
    if df[i].isnull().values.any() == True:
        print(i)