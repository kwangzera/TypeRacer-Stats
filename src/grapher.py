from datetime import datetime
from collections import defaultdict
from itertools import accumulate

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mplcursors

from .scraper import *

# Raw data
data = main_scrape()

# Graphed variables
wpm = data["wpm"]
date = [datetime.strptime(i, "%Y-%m-%d") for i in data["date"]]
wpm_avg = []
date_avg = []
cum_avg = []
run_avg = []

# Helper variables
total_races = len(wpm)
avg_of_day = defaultdict(list)
race_number = list(range(1, len(wpm)+1))
cum_wpm = [0] + list(accumulate(wpm))


def cumulative_average():
    """ Gets the cumulative average of all races """

    for idx, wpm in enumerate(cum_wpm[1:], start=1):
        cum_avg.append(wpm/idx)


def running_average(n):
    """ Gets the running average of last `n` races """

    # Invalid positions fill with None
    for _ in range(n-1):
        run_avg.append(None)

    # Average of last `n` races, querying with a prefix sum array
    for i in range(n, total_races+1):
        run_avg.append((cum_wpm[i]-cum_wpm[i-n]) / n)


def which_average(n):
    """ Returns running average of last `n` races. If `n` is invalid, return the cumulative average of all races """

    # Out of range, returning cumulative average
    if n <= 1 or n >= total_races:
        cumulative_average()
        return cum_avg, "Cumulative Average of All Races"

    # In Range, returning running average
    running_average(n)
    return run_avg, f"Running Average of {n} Races"


def daily_average():
    """ For each unique day, map it to a list of races for its corresponding day """

    # My hardcoded TypingClub stats
    if USERNAME == "username_example125259":
        avg_of_day[datetime(2018, 9, 17)].append(45.0)
        avg_of_day[datetime(2018, 10, 30)].append(54.0)
        avg_of_day[datetime(2018, 11, 19)].append(50.0)

    for w, dt in zip(wpm, date):
        avg_of_day[dt].append(w)

    for dt, races in avg_of_day.items():
        date_avg.append(dt)
        wpm_avg.append(sum(races)/len(races))


def scatterplot(x, y):
    """ Function to plot WPM vs. Race Number scatterplot graph """

    # Unpack figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.tight_layout(pad=6)

    # Unpack running average with respective label
    r_avg, avg_label = which_average(int(sys.argv[2]))

    # Customizing plot area
    color_cycle = ax._get_lines.prop_cycler
    ax.scatter(x, y, s=10, color=next(color_cycle)["color"], alpha=0.25)
    ax.plot(x, r_avg, color=next(color_cycle)["color"])
    ax.legend(labels=[avg_label, "Single Race"], loc="lower right")
    ax.set_axisbelow(True)

    # Customizing the Axes
    ax.set_title(f"WPM vs. Race Number for {USERNAME}")
    ax.set_xlabel("Race Number")
    ax.set_ylabel("WPM")

def lineplot(x, y):
    """ Function to plot Daily Average WPM line graph """

    # Unpack figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.tight_layout(pad=6)

    # Customizing plot area
    ax.plot(x, y, linewidth=0.5)
    dots = ax.scatter(x, y, color="none")
    ax.set_axisbelow(True)

    # Customizing the Axes
    ax.set_title(f"Daily Average WPM for {USERNAME}")
    ax.set_xlabel("Date")
    ax.tick_params("x", labelrotation=45)  # Make sure x-axis lables don't collide
    ax.set_ylabel("WPM")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    # Show annotations on hover
    crs = mplcursors.cursor(dots, hover=True)
    crs.connect("add", lambda sel: sel.annotation.set_text(
        f"{y[sel.target.index]:.1f} WPM average on {x[sel.target.index].strftime('%Y-%m-%d')}")
    )


def main_plot():
    """ Gets lists for daily average and plots both graphs at the same time """

    # Convert keys and values from daily average dict to lists
    daily_average()

    print("Graphing plots")
    plt.style.use("seaborn-darkgrid")  # Gridlines comes with the theme
    scatterplot(race_number, wpm)
    lineplot(date_avg, wpm_avg)
    plt.show()
