import json

import requests
from bs4 import BeautifulSoup

DEFAULT = {"wpm": [], "date": []}
USERNAME = "username_example125259"
URL = f"http://typeracerdata.com/profile?username={USERNAME}"
PATH = f"raw\\{USERNAME}.json"


def soup_all(url):
    """ returns a list containing all tables from typeracerdata.com with class=profile """
    link = requests.get(url)
    soup = BeautifulSoup(link.content, "html.parser")
    return soup.find_all("table", {"class": "profile"})


def get_userdata():
    """ Opens the userdata json file for reading and returns a dict with race data """

    with open(PATH, 'r') as f:
        return json.load(f)


def get_total_races(url):
    """ Gets the total number of races - first element of the first table """

    table = soup_all(url)
    return int(table[0].find("td").text.replace(",", ""))


def main_scrape():
    """ Main method for the scraping """

    # Set userdata as DEFAULT if file does not exist or empty
    try:
        userdata = get_userdata()
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        userdata = DEFAULT

    total_races = get_total_races(URL)
    last_race = len(userdata["wpm"])
    diff = total_races - last_race

    # By default typeracerdata.com loads the last 20 races when `diff` = 0
    if diff > 0:
        print(f"Caching last {diff} races for {USERNAME}")

        # Efficient caching - loading only the last `diff` races, cached races won't be loaded again
        table = soup_all(URL+f"&last={diff}")
        list_stats = table[-2].find_all("td")

        # Appending only the last `diff` races to dict
        for i in range(1, len(list_stats)+1, 7):
            date = list_stats[-i-5].text.split(" ")[0]
            wpm = float(list_stats[-i-4].text.replace(",", ""))
            userdata["wpm"].append(wpm)
            userdata["date"].append(date)

        # Write new modified userdata contents to file, overwriting previous contents
        with open(PATH, 'w') as file_write:
            json.dump(userdata, file_write)

    else:
        print(f"Cached data for {USERNAME} has already is up to date")

    return userdata
