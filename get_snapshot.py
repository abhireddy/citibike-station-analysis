import urllib.request
import json
import datetime

# get snapshot of JSON from real-time feed
url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode('utf-8'))

# set directory for file storage
folder = "json"
filename = "citibike " + str(datetime.datetime.utcnow()) + ".txt"
filepath = folder + "/" + filename

# store snapshot in directory
with open(filepath, 'w') as f:
  json.dump(data, f, ensure_ascii=False)
