# Import the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing the raw / uncleaned dataset
dataset = pd.read_csv('movie_metadata.csv')
data = dataset.loc[:, ['director_facebook_likes', 'actor_1_facebook_likes', 'actor_2_facebook_likes', 'actor_3_facebook_likes','cast_total_facebook_likes','movie_facebook_likes','gross','num_critic_for_reviews','num_voted_users','budget','imdb_score']].values

# Dropping inconsistent data
for i in range(data.shape[1]):
    drop = np.where(pd.isna(data[:, i]))
    drop = drop[0]
    data = np.delete(data, drop, axis = 0)

# Handling Missing Values
from sklearn.impute import SimpleImputer
missingvalues = SimpleImputer(missing_values=0.0, strategy = 'mean', verbose=0)
data = missingvalues.fit_transform(data)

# Seperating the independent and dependent variables
X = data[:,:-1]
y = data[:, -1]

# Seperating training and test datasets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Applying PCA to extract features from the huge dataset
from sklearn.decomposition import PCA
pca = PCA()
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

# Fitting the Random Forest Regression to the dataset
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators=1000, random_state=0)
regressor.fit(X_train,y_train)

# Predicting the result for the Test Set
y_pred = regressor.predict(X_test)

#Calculating the loss/error for the Test Set 
from sklearn.metrics import mean_squared_error
loss = mean_squared_error(y_pred,y_test)
print('Mean Squared Error = {:.2f}'.format(loss))