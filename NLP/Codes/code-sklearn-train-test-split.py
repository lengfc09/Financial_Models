# This script shows how to split up your data into training and
# testing subsets.
import numpy as np
from sklearn.model_selection import train_test_split
# Create data that is for illustration evenly-spaced.
X, y = np.arange(10).reshape((5, 2)), range(5)
X
list(y)
# Split up the data. `test_size` is the proportion of the dataset to
# be included in the test split. `random_state` is the seed of the
# random number generator (so that you get reproducible results when
# you run the code the next time).
X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.33, random_state=42)
# Take a look at the training set.
X_train
y_train
# Take a look at the test set.
X_test
y_test
# Alternative way to split up the data. Do NOT shuffle the data before
# splitting.
train_test_split(y, shuffle=False)
