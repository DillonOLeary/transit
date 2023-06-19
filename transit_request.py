import requests
import os
import datetime
import json

api_key = os.environ["ONEBUSAWAY_API_KEY"]


r = requests.get(f"http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_990003.json?key={api_key}")
r = r.json()

keys_of_interest = ["routeShortName", "tripHeadsign", "stopId", "scheduledArrivalTime", "predictedArrivalTime"]

filtered_response = []

for elem in r["data"]["entry"]["arrivalsAndDepartures"]:
    filtered_elem = {key: elem[key] for key in keys_of_interest}

    filtered_elem["scheduledArrivalTime"] = datetime.datetime.fromtimestamp(filtered_elem["scheduledArrivalTime"]/1000.0).ctime()
    if filtered_elem["predictedArrivalTime"] != 0:
        filtered_elem["predictedArrivalTime"] = datetime.datetime.fromtimestamp(filtered_elem["predictedArrivalTime"]/1000.0).ctime()
    else:
        filtered_elem["predictedArrivalTime"] = "no data"
    filtered_response.append({key: filtered_elem[key] for key in keys_of_interest})

print("Transit Data Filtered Results")
print(json.dumps(filtered_response, indent=4, sort_keys=True, default=str))
