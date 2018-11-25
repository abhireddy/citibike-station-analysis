import pandas as pd

df = pd.read_csv('csv/merged_snapshots.csv')

# filter for September '18 snapshots only
df = df[(df['last_updated'] >= '2018-09-01') & (df['last_updated'] < '2018-10-01')]

# add fields needed to grouping snapshots by time of day
df['day_of_week'] = pd.to_datetime(df['last_updated']).dt.dayofweek
df['last_updated_trunc'] = pd.to_datetime(df['last_updated']).dt.floor('h')
df['last_updated_hour'] = pd.DatetimeIndex(df['last_updated_trunc']).hour

# set time periods: weekday mornings (7-10 AM), weekday evenings (5-7 PM), weekends (9 AM - 9 PM)
df['time_of_day'] = "Other"
df['time_of_day'][(df['day_of_week'] <= 4) & (df['last_updated_hour'] >= 7) & (df['last_updated_hour'] < 10)] = "Peak Weekday Mornings"
df['time_of_day'][(df['day_of_week'] <= 4) & (df['last_updated_hour'] >= 17) & (df['last_updated_hour'] < 19)] = "Peak Weekday Evenings"
df['time_of_day'][(df['day_of_week'] >= 5) & (df['last_updated_hour'] >= 9) & (df['last_updated_hour'] < 21)] = "Peak Weekends"

# create fields for calculating % uptime/availability
df['time_interval'] = 10 # each snapshot represents a 10-minute interval
df['bike_uptime'] = 10
df['dock_uptime'] = 10
df['bike_uptime'][df['num_bikes_available'] <= 0] = 0 # count as downtime if no bikes available
df['dock_uptime'][df['num_docks_available'] <= 0] = 0  # count as downtime if no docks available

# group snapshots by station and time period
df_grp = df.groupby(['station_id','time_of_day']).sum()
df_grp['bike_uptime'] = df_grp['bike_uptime'] / df_grp['time_interval'] # 10-minute snapshots with uptime / total 10-minute snapshots
df_grp['dock_uptime'] = df_grp['dock_uptime'] / df_grp['time_interval']

# get additional station metadata (e.g. lat/long, station name, station status)
import urllib.request
import json

url = "https://feeds.citibikenyc.com/stations/stations.json"
response = urllib.request.urlopen(url)
unparsed = json.loads(response.read().decode('utf-8'))
data = unparsed['stationBeanList']
df2 = pd.DataFrame(data)

# merge grouped snapshots with station metadata
df_final = pd.merge(df_grp, df2, left_on="station_id", right_on="id", how="left")

# store results as CSV
df_final.to_csv('csv/station-availability-sept-18.csv', header=True)
