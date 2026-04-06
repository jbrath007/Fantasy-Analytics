import pandas as pd # Importing the pandas library for data manipulation and analysis
import os
#print(pd.__version__) # Printing the version of pandas being used

# Defining the URL for data from the 2023 season in parquet, could use .csv file as well but parquet is more efficient for larger datasets
url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"

roster = pd.read_parquet("https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_2025.parquet")

#print(roster.columns) # Printing the column names of the roster DataFrame to understand its structure and contents
# Reading the parquet file from the URL into a pandas DataFrame
data_frame_season = pd.read_parquet(url) 

#making sure the data is not missing
data_frame_season = data_frame_season[
       (data_frame_season["passer_player_name"].notna()) |
       (data_frame_season["rusher_player_name"].notna()) |
       (data_frame_season["receiver_player_name"].notna())
]

# collecting regular season stats
regular_season_data = data_frame_season[data_frame_season["season_type"] == "REG"]
#postseason_data = data_frame_season[data_frame_season["season_type"] == "POST"]

"""qb_rows = data_frame_season[data_frame_season["passer_player_id"].notna()]
print(qb_rows.columns[qb_rows.notna().any()].tolist()) 

rb_rows = data_frame_season[data_frame_season["rusher_player_id"].notna()]
print(rb_rows.columns[rb_rows.notna().any()].tolist()) 

wr_rows = data_frame_season[data_frame_season["receiver_player_id"].notna()]
print(wr_rows.columns[wr_rows.notna().any()].tolist()) """

# Printing the column names of the qb_rows DataFrame that contain non-null values to identify which columns have valid data for quarterbacks


# Filtering the DataFrame to include only rows where at least one of the following columns is not null: "passer_player_name", "rusher_player_name", or "receiver_player_name". This ensures that we are only working with rows that have valid player information for passing, rushing, or receiving.
qb_pass_frame = regular_season_data.groupby("passer_player_id").agg({
        "complete_pass": "sum",
        "passing_yards": "sum",
        "pass_touchdown": "sum",
        "interception": "sum",
        "fumble": "sum"
}).reset_index()

# Filtering the DataFrame to include only rows where the "pass_attempt" column is equal to 1, which indicates that a pass was attempted. Then, grouping the data by "passer_player_name" and aggregating the passing yards, passing touchdowns, and interceptions by summing them up for each player. Finally, resetting the index of the resulting DataFrame.
qb_pass_frame.columns = ["passer_player_id", "completions", "pass_yards", "pass_td", "ints", "fumble"]

qb_rush_frame = regular_season_data.groupby("rusher_player_id").agg({
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum"
}).reset_index()

qb_rush_frame.columns = ["rusher_player_id", "rush_attempt", "rush_yards", "rush_td"]

qb_data_frame = qb_pass_frame.merge(qb_rush_frame, left_on="passer_player_id", right_on="rusher_player_id", how="left").drop(columns=["rusher_player_id"])

# filtering the dataframe to include only row with a rush attempt and grabbing the rushing yards and  rushing touchdowns from those rows
rb_rushing_frame = regular_season_data.groupby("rusher_player_id").agg({
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum",
        "fumble": "sum"
}).reset_index()

# filtering the dataframe to include data where the running back was a receiver
rb_receiving_frame = regular_season_data.groupby("receiver_player_id").agg({
        "pass_attempt": "sum",
        "complete_pass": "sum",
        "receiving_yards": "sum",
        "pass_touchdown": "sum",
        "yards_after_catch": "sum"
}).reset_index()

# merging the rushing and receiving dataframes to create the running back table
rb_data_frame = rb_rushing_frame.merge(rb_receiving_frame, left_on="rusher_player_id", right_on="receiver_player_id", how="left").drop(columns=["receiver_player_id"])
rb_data_frame.columns = ["rusher_player_id", "rush_attempt","rush_yards", "rush_td", "fumble", "targets", "rec", "rec_yards", "rec_td",  "yac"]

# filtering the dataframe to include only rows where a receiver caught a pass
receiver_receiving_frame = regular_season_data.groupby("receiver_player_id").agg({
        "pass_attempt": "sum",
        "complete_pass": "sum",
        "receiving_yards": "sum",
        "pass_touchdown": "sum",
        "yards_after_catch": "sum",
        "fumble": "sum"
        
}).reset_index()

# filtering the dataframe to include only rows where a receiver had a rushing attempt
receiver_rushing_frame = regular_season_data.groupby("rusher_player_id").agg({
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum"
}).reset_index()

# merging the two dataframes for receiver stats into one table and dropping the rushing id
receiver_data_frame = receiver_receiving_frame.merge(receiver_rushing_frame, left_on="receiver_player_id", right_on="rusher_player_id", how="left").drop(columns=["rusher_player_id"])

# creating the column names for the receiver table
receiver_data_frame.columns = ["receiver_player_id", "targets", "rec", "rec_yards", "rec_td", "yac", "fumble", "rush_attempt", "rush_yards", "rush_td"]

#dropping any empty rows that dont exist in the relevant dataframe for each postion
qb_data_frame = qb_data_frame.dropna(subset=["passer_player_id"])
rb_data_frame = rb_data_frame.dropna(subset=["rusher_player_id"])
receiver_data_frame = receiver_data_frame.dropna(subset=["receiver_player_id"])

#keeping separate positional dataframes
qb_data_frame = qb_data_frame.merge(roster[["gsis_id", "full_name", "position", "team"]], left_on="passer_player_id", right_on="gsis_id", how="left")
rb_data_frame = rb_data_frame.merge(roster[["gsis_id", "full_name", "position", "team"]], left_on="rusher_player_id", right_on="gsis_id", how="left")
receiver_data_frame = receiver_data_frame.merge(roster[["gsis_id", "full_name", "position", "team"]], left_on="receiver_player_id", right_on="gsis_id", how="left")

# filling any missing values with 0, since if a player doesn't have stats in a category
qb_data_frame = qb_data_frame.fillna(0) 
rb_data_frame = rb_data_frame.fillna(0)
receiver_data_frame = receiver_data_frame.fillna(0)

# creating a rudimentary fantasy point calculation for qb
def qb_fantasy_points(row):
    return(
        row["pass_yards"] * 0.04 + 
        row["pass_td"] * 4 + 
        row["completions"]* 0.1 -
        row["ints"] * 2 + 
        row["rush_yards"] * 0.1 + 
        row["rush_td"] * 6 -
        row["fumble"] * 2
    )

# creating a crude fantasy point calculation for all other positions excluding qb stats since its very rare 
def fantasy_points(row):
    return(
        row["rush_yards"] * 0.1 + 
        row["rush_td"] * 6 + 
        row["rec_yards"] * 0.1 + 
        row["rec_td"] * 6 +
        row["rec"] * 0.5 -
        row["fumble"] * 2
    )

# applying the fantasy_points function to each row of the DataFrame to calculate the fantasy points for each player based on their stats
qb_data_frame["fantasy_points"] = qb_data_frame.apply(qb_fantasy_points, axis=1)
rb_data_frame["fantasy_points"] = rb_data_frame.apply(fantasy_points, axis=1)
receiver_data_frame["fantasy_points"] = receiver_data_frame.apply(fantasy_points, axis=1)

# spliting by position
qb_pos = qb_data_frame[qb_data_frame["position"] == "QB"]
rb_pos = rb_data_frame[rb_data_frame["position"] == "RB"]
wr_pos = receiver_data_frame[receiver_data_frame["position"] == "WR"]
te_pos = receiver_data_frame[receiver_data_frame["position"] == "TE"]

# cleaning data
qb_stats = qb_pos[["full_name", "team", "position", "completions", "pass_yards", "pass_td", "ints", "rush_attempt", "rush_yards", "rush_td", "fumble", "fantasy_points"]]
rb_stats = rb_pos[["full_name", "team", "position", "rush_attempt", "rush_yards", "rush_td", "targets", "rec", "rec_yards", "rec_td", "yac", "fumble", "fantasy_points"]]
wr_stats = wr_pos[["full_name", "team", "position", "targets", "rec", "rec_yards", "rec_td", "yac", "rush_attempt", "rush_yards", "rush_td", "fumble", "fantasy_points"]]
te_stats = te_pos[["full_name", "team", "position", "targets", "rec", "rec_yards", "rec_td", "yac", "rush_attempt", "rush_yards", "rush_td", "fumble", "fantasy_points"]]

#file management for excel output
file_path = "Fantasy_Stats_2025.xlsx"

# if the file exists append it if not create a new one 
mode = 'a' if os.path.exists(file_path) else 'w'
if_sheet_exists = "replace" if mode == 'a' else None

# create several sheets in an excel file splitting by position and sorting them by most fantasy points scored
with pd.ExcelWriter("Fantasy_Stats_2025.xlsx", engine="openpyxl", mode=mode, if_sheet_exists=if_sheet_exists) as writer:
    qb_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Quarterbacks", index = False)
    rb_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Running Backs", index = False)
    wr_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Wide Receivers", index = False)
    te_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Tight Ends", index = False)

print("Data Successfully Processed and Exported to Excel Sheet!")