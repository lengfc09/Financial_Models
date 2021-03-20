import var_ntime

import scipy.stats as stats

mydf = stats.t.rvs(loc=0, scale=0.5, df=5, size=10000)
print(stats.stats.describe(mydf))
print(stats.t.stats(loc=0, scale=0.5, df=5, moments="mvsk"))
var_ntime.myvar(mydf)
var_ntime.myhist(mydf, bins=300)
print(stats.norm.fit(mydf))

print(stats.t.fit(mydf))
