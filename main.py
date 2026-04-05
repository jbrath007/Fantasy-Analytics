import pandas as pd # Importing the pandas library for data manipulation and analysis
import os
print(pd.__version__) # Printing the version of pandas being used

# Defining the URL for data from the 2023 season in parquet, could use .csv file as well but parquet is more efficient for larger datasets
url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"

roster = pd.read_parquet("https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_2025.parquet")

#print(roster.columns) # Printing the column names of the roster DataFrame to understand its structure and contents
# Reading the parquet file from the URL into a pandas DataFrame
data_frame_season = pd.read_parquet(url) 
#data_frame_season = pd.read_csv(url) # If using the CSV file instead of parquet

#making sure the data is not missing
data_frame_season = data_frame_season[
       (data_frame_season["passer_player_name"].notna()) |
       (data_frame_season["rusher_player_name"].notna()) |
       (data_frame_season["receiver_player_name"].notna())
]
# Filtering the DataFrame to include only rows where at least one of the following columns is not null: "passer_player_name", "rusher_player_name", or "receiver_player_name". This ensures that we are only working with rows that have valid player information for passing, rushing, or receiving.
qb_data_frame = data_frame_season.groupby("passer_player_id").agg({
        "passing_yards": "sum",
        "pass_touchdown": "sum",
        "interception": "sum",
        "complete_pass": "sum",
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum"

}).reset_index()

# Filtering the DataFrame to include only rows where the "pass_attempt" column is equal to 1, which indicates that a pass was attempted. Then, grouping the data by "passer_player_name" and aggregating the passing yards, passing touchdowns, and interceptions by summing them up for each player. Finally, resetting the index of the resulting DataFrame.
qb_data_frame.columns = ["passer_player_id", "pass_yards", "pass_td", "ints", "completions", "rush_attempt", "rush_yards", "rush_td"]

# filtering the dataframe to include only row with a rush attempt and grabbing the rushing yards and  rushing touchdowns from those rows
rb_data_frame = data_frame_season.groupby("rusher_player_id").agg({
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum",
        "receiving_yards": "sum",
        "pass_touchdown": "sum",
        "complete_pass": "sum",
        "yards_after_catch": "sum",
        "pass_attempt": "sum"
}).reset_index()

rb_data_frame.columns = ["rusher_player_id", "rush_attempts","rush_yards", "rush_td", "rec_yards", "rec_td", "rec", "yac", "targets"]

# filtering the dataframe to include only row
receiver_data_frame = data_frame_season.groupby("receiver_player_id").agg({
        "receiving_yards": "sum",
        "pass_touchdown": "sum",
        "complete_pass": "sum",
        "yards_after_catch": "sum",
        "pass_attempt": "sum",
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum"
        
}).reset_index()

receiver_data_frame.columns = ["receiver_player_id", "rec_yards", "rec_td", "rec", "yac", "targets", "rush_attempts", "rush_yards", "rush_td"]

qb_data_frame = qb_data_frame.dropna(subset=["passer_player_id"])
rb_data_frame = rb_data_frame.dropna(subset=["rusher_player_id"])
receiver_data_frame = receiver_data_frame.dropna(subset=["receiver_player_id"])

#keeping separate positional dataframes
qb_data_frame = qb_data_frame.merge(roster[["gsis_id", "full_name", "position"]], left_on="passer_player_id", right_on="gsis_id", how="left")
rb_data_frame = rb_data_frame.merge(roster[["gsis_id", "full_name", "position"]], left_on="rusher_player_id", right_on="gsis_id", how="left")
receiver_data_frame = receiver_data_frame.merge(roster[["gsis_id", "full_name", "position"]], left_on="receiver_player_id", right_on="gsis_id", how="left")

# filling any missing values with 0, since if a player doesn't have stats in a category
qb_data_frame = qb_data_frame.fillna(0) 
rb_data_frame = rb_data_frame.fillna(0)
receiver_data_frame = receiver_data_frame.fillna(0)

def qb_fantasy_points(row):
    return(
        row["pass_yards"] * 0.04 + 
        row["pass_td"] * 4 + 
        row["completions"]* 0.1 -
        row["ints"] * 2 + 
        row["rush_yards"] * 0.1 + 
        row["rush_td"] * 6 
    )

def fantasy_points(row):
    return(
        row["rush_yards"] * 0.1 + 
        row["rush_td"] * 6 + 
        row["rec_yards"] * 0.1 + 
        row["rec_td"] * 6 +
        row["rec"] * 0.5
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
qb_stats = qb_pos[["full_name", "position", "pass_yards", "pass_td", "completions", "ints", "rush_yards", "rush_td", "fantasy_points"]]
rb_stats = rb_pos[["full_name", "position", "rush_yards", "rush_td", "rec_yards", "rec_td", "rec", "yac", "targets", "fantasy_points"]]
wr_stats = wr_pos[["full_name", "position", "rec_yards", "rec_td", "rec", "yac", "targets", "fantasy_points"]]
te_stats = te_pos[["full_name", "position", "rec_yards", "rec_td", "rec", "yac", "targets", "fantasy_points"]]

#file management for excel output
file_path = "Fantasy_Stats_2025.xlsx"

mode = 'a' if os.path.exists(file_path) else 'w'

if_sheet_exists = "replace" if mode == 'a' else None

with pd.ExcelWriter("Fantasy_Stats_2025.xlsx", engine="openpyxl", mode=mode, if_sheet_exists=if_sheet_exists) as writer:
    qb_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Quarterbacks", index = False)
    rb_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Running Backs", index = False)
    wr_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Wide Receivers", index = False)
    te_stats.sort_values(by="fantasy_points", ascending=False).to_excel(writer, sheet_name="Tight Ends", index = False)


# Printing the column names of the DataFrame to understand the structure of the data
#print("Here are the DataFrame Stats: \r")
#print(data_frame_stats.columns) 

# Printing the first few rows of the DataFrame to get a glimpse of the data and its contents
#print(data_frame_stats.head())

