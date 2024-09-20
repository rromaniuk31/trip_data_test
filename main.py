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
            
    for i in cols:
        temp_col = i + "_temp"
        df[temp_col] = -1
        for j in range(0, len(df[temp_col])):
            dec_loc = df[i][j].find(".", 0, 3)
            if dec_loc == 1:
                adj_hours = int(df[i][j][2:4]) + 24 * int(df[i][j][0:1])
                df[temp_col][j] = str(adj_hours) + df[i][j][4:]
            elif dec_loc == 2:
                adj_hours = int(df[i][j][3:5]) + 24 * int(df[i][j][0:2])
                df[temp_col][j] = str(adj_hours) + df[i][j][5:]
            else:
                df[temp_col][j] = df[i][j]
        
        
        new_sec_col = i + "_seconds"
        df[new_sec_col] = pd.to_timedelta(df[temp_col]).dt.total_seconds()
        
        df = df.drop(temp_col, axis=1)
    return(df)

cols = ["afterHoursDrivingDuration", "afterHoursStopDuration", "drivingDuration", "idlingDuration", "speedRange1Duration", "speedRange2Duration", "speedRange3Duration", "stopDuration", "workDrivingDuration", "workStopDuration"]
seconds_df = convert_to_seconds(df, cols)

seconds_df.to_parquet('trip_data_withSeconds.parquet')


all_cols = list(df.columns)
for i in all_cols:
    if df[i].isnull().values.any() == True:
        print(i)