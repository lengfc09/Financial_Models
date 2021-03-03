# This script illustrates how to use the naive Bayes classifier from
# SciKit-Learn.
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics     # To evaluate model performance.
# Generate random data to work on. We don't expect any great results
# from naive Bayes here because the input data is just random. In
# reality, if there is some structure in the data, naive Bayes should
# (hopefully) be able to pick it up.
X = np.random.randint(5, size=(6, 100))
y = np.array([1, 2, 3, 3, 2, 1])
# Split up the data into training and testing.
count_train, count_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.33, random_state=42)
# Initialize our class. If the result is suboptimal, you can change
# the `alpha` parameter.
nb = MultinomialNB()            # MultinomialNP(alpha=0.5)
# Determine internal parameters based on dataset. Pass training count
# vectorizer first, and training labels second.
nb.fit(count_train, y_train)
# Get the class labels.
nb.classes_
# Log-probability of features occurring, given a class.
nb.coef_[0]
# Make predictions of the label for test data.
pred = nb.predict(count_test)
# Test accuracy of predictions.
metrics.accuracy_score(y_test, pred)
# The confusion matrix shows correct and incorrect labels. `labels`
# can be used to reorder the resulting matrix. On the ouput array, the
# main diagonal shows the true scores, i.e. the labels that have been
# correctly predicted. The true labels correspond to the rows while
# the predicted labels correspond to the columns. For example, if you
# have in the second row "sci-fi" and in the first column "action"
# (e.g. if you're looking at movie reviews), then the entry in the
# second row, first column shows you the number of movie reviews that
# are about sci-fi movies but were incorrectly classified as reviews
# of action movies.
metrics.confusion_matrix(y_test, pred, labels=[0, 1])
