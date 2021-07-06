
#%% 


from datetime import datetime
import pandas as pd
import numpy as np
from pandas.core import frame
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

# %%

def process_index_pivot(vi_link, v_index):

    v_index = str(v_index)

    vi_tbl = pd.read_csv(vi_link)

    vi_tbl['year'] = vi_tbl.month.astype(str).str[0:4]
    vi_tbl['month'] = vi_tbl.month.astype(str).str[5:7]

        
    vi_tbl = vi_tbl\
        .groupby(['year', 'month'])[v_index]\
            .aggregate('mean')\
                .unstack()\
                    .reset_index()

    vi_tbl.columns = v_index + "_" + vi_tbl.columns    
    
    vi_tbl.index = vi_tbl.index.astype(int)

    return vi_tbl


# %%

sa_evi = process_index_pivot('sa_all_polygons_evi.csv', 'EVI').set_index('EVI_year')
sa_ndsi = process_index_pivot('sa_all_polygons_ndsi.csv', 'NDSI').set_index('NDSI_year')
sa_nbr = process_index_pivot('sa_all_polygons_nbrt.csv', 'NBRT').set_index('NBRT_year')

sa_yield = pd.read_csv('sa_yield.csv', index_col = 'year')
sa_yield.index = sa_yield.index.astype(str)

sa_rain = pd.read_csv('sa_crop_rain.csv', index_col = 'year')
sa_rain.index = sa_rain.index.astype(str)

sa_rand_forrest_table = pd.concat([sa_evi, sa_ndsi, sa_nbr, sa_yield], axis = 1)

sa_rand_forrest_table = sa_rand_forrest_table[sa_rand_forrest_table.index != '2021'].fillna(method='bfill')

# %%

# Labels are the values we want to predict
labels = np.array(sa_rand_forrest_table['Yield'])

# Remove the labels from the features
# axis 1 refers to the columns
features = sa_rand_forrest_table.drop(['Yield', 'production', 'hectares'], axis = 1)

# Saving feature names for later use
feature_list = list(features.columns)

# Convert to numpy array
features = np.array(features)


# %%


# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = \
    train_test_split(features, 
                     labels, 
                     test_size = 0.25, 
                     random_state = 42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

# %%

# Import the model we are using
from sklearn.ensemble import RandomForestRegressor

# Instantiate model with 1000 decision trees

rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)

# Train the model on training data
rf.fit(train_features, train_labels)

# %%

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)

# Calculate the absolute errors
errors = abs(predictions - test_labels)

# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'tonnes per hectare.')


# %%

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


# %%

# Import tools needed for visualization
from sklearn.tree import export_graphviz
import pydot

# Pull out one tree from the forest
tree = rf.estimators_[5]

# Import tools needed for visualization
from sklearn.tree import export_graphviz
import pydot

# Pull out one tree from the forest
tree = rf.estimators_[5]

# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', 
                feature_names = feature_list, 
                rounded = True, 
                precision = 1)

# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')

# Write graph to a png file
# graph.write_png('tree.png')

# %%

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

# %%

# Import matplotlib for plotting and use magic command for Jupyter Notebooks
import matplotlib.pyplot as plt

# Set the style
plt.style.use('fivethirtyeight')

# list of x locations for plotting
x_values = list(range(len(importances)))

# Make a bar chart
plt.bar(x_values, importances, orientation = 'vertical')

# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation='vertical')

# Axis labels and title
plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances')


