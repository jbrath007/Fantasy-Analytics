import pandas as pd # Importing the pandas library for data manipulation and analysis
print(pd.__version__) # Printing the version of pandas being used

# Defining the URL for data from the 2023 season in parquet, could use .csv file as well but parquet is more efficient for larger datasets
url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet"
#if using CSV file instead of parquet
#url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2023.csv"

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
qb = data_frame_season[data_frame_season["pass_attempt"]== 1].groupby("passer_player_name").agg({
        "passing_yards": "sum",
        "pass_touchdown": "sum",
        "interception": "sum",
        "complete_pass": "sum"
}).reset_index()

# Filtering the DataFrame to include only rows where the "pass_attempt" column is equal to 1, which indicates that a pass was attempted. Then, grouping the data by "passer_player_name" and aggregating the passing yards, passing touchdowns, and interceptions by summing them up for each player. Finally, resetting the index of the resulting DataFrame.
qb.columns = ["player", "pass_yards", "pass_td", "ints", "completions"]

# filtering the dataframe to include only row with a rush attempt and grabbing the rushing yards and  rushing touchdowns from those rows
rb = data_frame_season[data_frame_season["rush_attempt"]== 1].groupby("rusher_player_name").agg({
        "rush_attempt": "sum",
        "rushing_yards": "sum",
        "rush_touchdown": "sum"
}).reset_index()

rb.columns = ["player", "rush_attempts","rush_yards", "rush_td"]

# filtering the dataframe to include only row
wr = data_frame_season[data_frame_season["complete_pass"]== 1].groupby("receiver_player_name").agg({
        "receiving_yards": "sum",
        "pass_touchdown": "sum",
        "complete_pass": "sum",
        "yards_after_catch": "sum",
        "pass_attempt": "sum"
}).reset_index()

wr.columns = ["player", "rec_yards", "rec_td", "rec", "yac", "targets"]

# merging everything together into one dataframe
data_frame_stats = qb.merge(rb, on="player", how="outer")
data_frame_stats = data_frame_stats.merge(wr, on="player", how="outer")

data_frame_stats = data_frame_stats.fillna(0) # filling any missing values with 0, since if a player doesn't have stats in a category

def fantasy_points(row):
    return(
        row["pass_yards"] * 0.04 + 
        row["pass_td"] * 4 + 
        row["completions"]* 0.1 +
        row["ints"] * -2 + 
        row["rush_yards"] * 0.1 + 
        row["rush_td"] * 6 + 
        row["rec_yards"] * 0.1 + 
        row["rec_td"] * 6 +
        row["rec"] * 0.5
    )
# applying the fantasy_points function to each row of the DataFrame to calculate the fantasy points for each player based on their stats
data_frame_stats["fantasy_points"] = data_frame_stats.apply(fantasy_points, axis=1)
# Printing the column names of the DataFrame to understand the structure of the data
print("Here are the DataFrame Stats: \r")
#print(data_frame_stats.columns) 

# Printing the first few rows of the DataFrame to get a glimpse of the data and its contents
print(data_frame_stats.head())

