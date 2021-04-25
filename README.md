# TypeRacer Stats
Python program to generate graphs of WPM vs. Race Number and Daily Average WPM.

![WPM vs. Race Number](https://github.com/Togohogo1/TypeRacer-Stats/blob/main/screenshots/WPM_vs_Race_Number.png)\
![Daily Average WPM](https://github.com/Togohogo1/TypeRacer-Stats/blob/main/screenshots/Daily_Average_WPM.png)

### Setup
This program assumes that the specified user has a [TypeRacer](https://play.typeracer.com/) account along with an imported profile on [typeracerdata.com](http://typeracerdata.com/). This program also assumes that the user's typeracerdata.com profile is updated to match the statistics on the main TypeRacer website.

Once downloaded, double-click `run.bat` to start the program. All necessary libraries will be installed in a virtual environment.

### WPM vs. Race Number
This graph displays a scatterplot showing all races of a user. Additionally, a trendline may be plotted displaying either the running average of the last `n` races or the cumulative average of all races. Hovering over a point does not show an annotation for this graph.

### Daily Average WPM
This graph displays a line graph showing a user's daily average over time. Hovering over a point will show an annotation displaying the user's daily average on a specific date.

### Passing Arguments
Running this program requires passing 2 arguments shown in the order shown below:
```bash
python -m src [TypeRacer Username] [Average of Last n Races]
```

If the `Average of Last n Races` parameter is less than or equal to one or greater than the total number of a user's races, then the cumulative average of all races will be plotted.
