import os
import json
import pandas as pd

def getData(path):
    with open(path, "r") as read_file:
        raw_data = json.load(read_file)

    # get station-level metrics
    data = raw_data['data']['stations']
    df = pd.DataFrame(data)

    # add snapshot timestamp to dataframe
    lastUpdated = raw_data['last_updated']
    df['last_updated'] = pd.to_datetime(lastUpdated,unit='s')

    return df

# set snapshot directory
dir = 'json'
arr = os.listdir(dir)

first = True # determines whether to create new df or append to existing

for file in arr:
    if file != '.DS_Store':
        path = dir + '/' + file
        df2 = getData(path)

        if first == True: # for first iteration, create new dataframe
            df = df2
            first = False
        else: # for subsequent iterations, append to existing dataframe
            frames = [df,df2]
            df = pd.concat(frames, ignore_index=True, sort=False)

        print("merged  " + file) # helps track progress since script takes several minutes to run

df.to_csv('csv/merged_snapshots.csv', index=False, header=True)
