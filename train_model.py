from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

#linking data_frame_stats from main.py to train a model
from main import data_frame_stats

# Selecting the features and target variable for the model. 
# The features are the columns "pass_yards", "rush_yards", and "rec_yards", which represent the passing yards, rushing yards, and receiving yards of the players, respectively. 
# The target variable is "fantasy_points", which represents the fantasy points scored by the players based on their stats.
features = ["pass_yards", "rush_yards", "rec_yards"]
target = "fantasy_points"
# Selecting the features (pass_yards, rush_yards, rec_yards) and the target variable (fantasy_points) from the data_frame_stats DataFrame. 
# The features will be used to train the model, while the target variable will be what the model is trying to predict.
X = data_frame_stats[features]
Y = data_frame_stats[target]

# Splitting the dataset into training and testing sets using the train_test_split function from scikit-learn.
# The test size is set to 20% of the data, meaning that 80% of the data will be used for training the model and 20% will be used for testing its performance. 
# The resulting variables X_train, X_test, Y_train, and Y_test will contain the respective subsets of the features and target variable for training and testing.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2)

# Training a Random Forest Regressor model using the training data (X_train and Y_train). The model is initialized with 100 trees (n_estimators=100) and a random state of 42 for reproducibility.
# After fitting the model to the training data, it can be used to make predictions on the test set (X_test) and evaluate its performance.
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, Y_train)

print("Model Successfully Trained!")


