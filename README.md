
# The Perfect 11: Finding the best FPL team

For the 2022-23 English Premier League season more than 10,000,000 fantasy teams were created to play in the FPL. While most of these teams are built using individuals favourite players/teams, in this project I look to take a data science approach to the question of team building.

The goal of this project is to use historical FPL data supplimented with data from FBref.com to predict the best possible team for the start of the season.

## Methodology

![Model](https://github.com/AstroLebs/LHL_Final_Project/blob/main/output/figures/Modelling.png?raw=true)

The data is pulled from Vaastav's repo of historical data along with fbref.com, merged together, and then fed into my modelling pipeline. Once my model has predicted how many FPL points each player is going to score it is passed to an optimization function to find the perfect 11.

![Model](https://github.com/AstroLebs/LHL_Final_Project/blob/main/output/figures/Modelling%20(2).png?raw=true)

As players transfer in to the league and don't have previous years FPL stats the current model relies on the FPL's rank of all players above the advanced stats. Using this model though, I was able to produce the following team (Point total as of December 8, 2022).

![Results](https://github.com/AstroLebs/LHL_Final_Project/blob/main/output/figures/Results.png?raw=true)

## Current Limitations and Future Steps

As I continue to work on this project my goals are to:

* Integrate new player transfers into the league based on fbref.com's advanced stats
* Have the model take into account how a players team affects the individuals FPL point production (major transfers can dramatically change team dynamics)
* Account for the week-to-week transfers that the FPL allows for as well as different abilities

## Data Sources and Acknowledgements

[Fantasy Premier League](https://fantasy.premierleague.com)

[Historic FPL Data by Vaastav Anand](https://github.com/vaastav/Fantasy-Premier-League)

[FBRef.com](https://fbref.com)
