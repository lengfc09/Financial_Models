"""
Data Analysis Part - By Chen Yangyifan
In this part, we analyze the quots from "all_quots.pkl"
* We use PCA to find out the first 3 principle components.
* Analyze the economic meaning and distribution of the daily changes in these components.
* Analyze the value at risk of USDRMB with these components
"""


import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

quots = pd.read_pickle("all_quots.pkl")
quots.tail()

# Check the correlations
import seaborn as sns

corrs = quots.corr()
sns.heatmap(corrs, cmap="YlGnBu")

data = quots.dropna()

# Mean Normalization, so that the features centers in the original point
dmean = data.mean(axis=0)
dstd = data.std(axis=0)
data = (data - dmean) / dstd

# PCA
from numpy import linalg

U, sigma, VT = linalg.svd(1 / len(data) * np.dot(data.T, data))

# Components
components = pd.DataFrame(U.T, columns=data.columns)
components = components.T
components.columns = ["CP" + str(item + 1) for item in components.columns]

# Draw the components
components.plot(y=["CP1", "CP2", "CP3"])

# Check how much variation each component explains
# Total Variation
weights = []
var = np.sum(data.values.flatten() ** 2)
for i in range(1, 11):
    # Use the i-th components
    data_temp = np.dot(data, components[["CP{}".format(i)]])
    data_temp = np.dot(data_temp, components[["CP{}".format(i)]].T)

    # How much information captured
    var_temp = np.sum(data_temp.flatten() ** 2)
    weights.append(var_temp / var)

import matplotlib as mpl

mpl.style.use(["ggplot"])
plt.plot(components.columns, weights, "r*--")


#  reverse the Normalization process for Components
df_reverse = pd.concat([dmean, dstd], 1)
df_reverse.columns = ["dmean", "dstd"]
reverse_components = (components.T * df_reverse["dstd"] + df_reverse["dmean"]).T
reverse_components


def my_reverse(cps):
    # this function reverse the mean,normalization process above
    global df_reverse
    temp = (cps.T * df_reverse["dstd"] + df_reverse["dmean"]).T
    return temp


# For USD, lets see how much information is captured by the components/risk-factors:
quots.dropna().plot(y=["USD"])

# Approximation USDRMB.ex with the first Three components:
approx_3 = data.dot(components.iloc[:, :3]).dot(components.iloc[:, :3].T)
reverse_approx_3 = approx_3.apply(lambda t: my_reverse(t), axis=1)
plt.rcParams["figure.figsize"] = (10, 8)
plt.plot(quots_dropna["USD"])
plt.plot(reverse_approx_3["USD"])
plt.legend(["Real USDRMB.ex", "Appoximation With 3 components"])


# Approximation EUDRMB.ex with the first Three components:
plt.plot(quots_dropna["EUD"])
plt.plot(reverse_approx_3["EUD"])
plt.legend(["Real EUDRMB.ex", "Appoximation With 3 components"])

# Approximation AUDRMB.ex with the first Three components:
plt.plot(quots_dropna["AUD"])
plt.plot(reverse_approx_3["AUD"])
plt.legend(["Real AUD.ex", "Appoximation With 3 components"])


# Approximation JPYRMB.ex with the first Three components:
plt.plot(quots_dropna["NZD"])
plt.plot(reverse_approx_3["NZD"])
plt.legend(["Real NZDRMB.ex", "Appoximation With 3 components"])

# Regard the first 3-components as risk-factor
# Analyze the economic meaning and dristibution of these risk factor
risk_factors = data.dot(components.iloc[:, :3])
risk_factors.head()

# Economic Meaning
## # Draw the components
components.plot(y=["CP1", "CP2", "CP3"], marker="*", markersize=10)


# How these risk-fatocrs behave
risk_factors.plot(y=["CP1", "CP2", "CP3"])


import vars.var_ntime as nvar  # my own package for analyze the Vars

# How these risk-fatocrs changes on a daily basis
nvar.myhist(risk_factors["CP1"].diff().dropna())
nvar.myhist(risk_factors["CP2"].diff().dropna())
nvar.myhist(risk_factors["CP3"].diff().dropna())

# the correlation matrix of daily change in CP1\CP2\CP3
risk_factors.diff().dropna().corr()
# Covariance matrix of daily change in CP1,CP2,CP3
risk_factors.diff().dropna().cov()
# Cholesky decompostion
C = linalg.cholesky(risk_factors.diff().dropna().cov())

import scipy.stats as stats

print(
    "means for daily changes in 3 componets:\t",
    stats.describe(risk_factors.diff().dropna()).mean,
)
print(
    "variance for daily changes 3 componets:\t",
    stats.describe(risk_factors.diff().dropna()).variance,
)


# Use montecarlo simulation to analyze the daily Var
# Mainly use the first 3 risk-factors
def myvar(C, dstd, components, num_of_sim=10000):
    # COV=C*C'
    # dstd is the standard deviation of the real ex quots
    # num_of_sim is the number of simulation
    # componetns is the first 3 principle components of normalized ex quots
    result = pd.DataFrame(columns=quots_dropna.columns)
    for i in range(num_of_sim):
        # simulate daily change in risk factor
        # Use the covariance to capture the correlation involved
        rv = np.dot(C, stats.norm.rvs(size=3))
        # Use the change in risk-factor, back to the change in real exchange rates
        delta_ex = components.iloc[:, :3].dot(rv) * dstd
        result = result.append(delta_ex, ignore_index=True)

    return result


result = myvar(C, dstd, components)

# Vars from PCA （First 3 Componetns） and montecarlo simulation
final_vars = result.apply(lambda t: np.percentile(t, [1, 5, 10, 90, 95, 99]), axis=0)
final_vars.index = [str(item) + r"%" for item in [1, 5, 10, 90, 95, 99]]
final_vars

# From comparison, here is the Vars calculated for each individual real exchange rates
real_vars = (
    quots_dropna.diff()
    .dropna()
    .apply(lambda t: np.percentile(t, [1, 5, 10, 90, 95, 99]), axis=0)
)
real_vars.index = [str(item) + r"%" for item in [1, 5, 10, 90, 95, 99]]
real_vars
