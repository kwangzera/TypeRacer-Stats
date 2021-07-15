import json
import sys
from datetime import datetime

import requests

DEFAULT = {"wpm": [], "utc": []}
USERNAME = sys.argv[1]
URL = f"https://data.typeracer.com/games?playerId=tr:{USERNAME}&universe=play"
PATH = f"raw\\{USERNAME}.json"


def get_userdata():
    """ Opens the userdata json file for reading and returns a dict with race data """

    with open(PATH, 'r') as f:
        return json.load(f)


def get_total_races():
    """ Gets the total number of races """

    data = requests.get(URL+"&n=1").json()
    return data[0]["gn"]


def fetch_and_cache():
    """ Main method for fetching from the api and caching races """

    # Set userdata as DEFAULT if file does not exist or empty
    try:
        userdata = get_userdata()
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        userdata = DEFAULT

    total_races = get_total_races()
    last_race = len(userdata["wpm"])
    diff = total_races - last_race
    fromjson = []

    if diff > 0:
        print(f"{diff} race(s) to be cached for {USERNAME}")

        if diff <= 1000:
            loaded = requests.get(URL+f"&n={diff}").json()

            # Caching data
            for race in reversed(loaded):
                userdata["wpm"].append(race["wpm"])
                userdata["utc"].append(race["t"])

        else:
            # Offsetting `now` by an hour, Typeracer api uses UTC time
            now = datetime.utcnow().timestamp() + 3600

            # Load pages of 999 races, then load remaining
            while diff > 0:
                loaded = requests.get(URL+f"&startDate=0&endDate={now}").json()
                tot = 999 if diff > 999 else diff

                for i in range(tot):
                    fromjson.append((loaded[i]["wpm"], loaded[i]["t"]))

                now = loaded[-1]["t"]
                diff -= tot

                print(f"Caching in progress, {diff} race(s) remaining")

            # Caching data
            for wpm, utc in reversed(fromjson):
                userdata["wpm"].append(wpm)
                userdata["utc"].append(utc)

        # Write new modified userdata contents to file, overwriting previous contents
        with open(PATH, 'w') as file_write:
            json.dump(userdata, file_write)

    else:
        print(f"Cached data for {USERNAME} is already up to date")

    return userdata
