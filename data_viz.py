import pandas as pd
import matplotlib.pyplot as plt

#Read in data from csv
nflPassing = "nfl_passing.csv"
dfNflPassing = pd.read_csv(nflPassing)
nflRushing = "nfl_rushing.csv"
dfNflRushing = pd.read_csv(nflRushing)
nflWins = "nfl_wins.csv"
nflWins = pd.read_csv(nflWins)

#Aggregate up passing yds and attempts grouping by Team
dfNflPassingTeamTotal= dfNflPassing[["Team", "Yds", "Att"]]
dfNflPassingTeamTotal = dfNflPassingTeamTotal.rename(columns = {"Yds": "Passing Yds", "Att": "Passing Att"})
dfNflPassingTeamTotal = dfNflPassingTeamTotal.groupby("Team")[["Passing Yds", "Passing Att"]].sum()
#Calculate passing yards per attempt
dfNflPassingTeamTotal["Passing YPA"] = dfNflPassingTeamTotal["Passing Yds"] / dfNflPassingTeamTotal["Passing Att"]

#Aggregate up rushin yds and attempts grouping by Team
dfNflRushingTeamTotal= dfNflRushing[["Team", "Yds", "Att"]]
dfNflRushingTeamTotal = dfNflRushingTeamTotal.rename(columns = {"Yds": "Rushing Yds", "Att": "Rushing Att"})
dfNflRushingTeamTotal = dfNflRushingTeamTotal.groupby("Team")[["Rushing Yds", "Rushing Att"]].sum()
#Calculate rushing yards per attempt
dfNflRushingTeamTotal["Rushing YPA"] = dfNflRushingTeamTotal["Rushing Yds"] / dfNflRushingTeamTotal["Rushing Att"]

#Merge the three data sets
dfNflTeamTotals = nflWins.merge(dfNflPassingTeamTotal, how="inner", on="Team").merge(dfNflRushingTeamTotal, how="inner", on="Team")
dfNflTeamTotals.sort_values(by=['Team'], inplace=True)

#Draw some plots
columnList = ["Team", "Passing Yds", "Rushing Yds"]
dfNflTeamTotals[columnList].plot.bar(x="Team", rot=90, colormap='winter')
dfNflTeamTotals[columnList].plot.bar(x="Team", rot=90, stacked=True, colormap='winter')

scatterSize = dfNflTeamTotals["Wins"] * 20
dfNflTeamTotals.plot.scatter(x="Passing YPA", y="Rushing YPA", c="Wins", s=scatterSize, colormap='winter')
plt.show()
