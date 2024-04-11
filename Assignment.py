#!/usr/bin/env python3

import csv
import pandas as pd


# Read the data from the CSV file into a DataFrame
data=[]
with open("SBIN_Data.csv",'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Convert the list of dictionaries into a DataFrame
df=pd.DataFrame(data)

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format= '%d-%m-%Y')

# Define a function to calculate rank for each row
def calculate_rank(row, days=5):
    current_date = row['Date']
    current_time = row['Time']
    previous_dates = [current_date - pd.Timedelta(days=i) for i in range(1, days+1)]
    previous_volumes = []
    for date in previous_dates:
        same_minute_date = df[(df['Date'] == date) & (df['Time'] == current_time)]
        if not same_minute_date.empty:
            previous_volumes.extend(same_minute_date['Volume'])
    rank = sum(1 for volume in previous_volumes if volume > row['Volume']) + 1
    return rank
    

df['Rank']= df.apply(calculate_rank, axis=1)

df.to_csv("Output.csv", index=True)