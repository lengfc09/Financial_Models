def myes(df_input, alphas=[0.01, 0.05], num_of_simus=1000000, method="all", tell=True):
    if method not in ["all", "norm", "t", "historical"]:
        print("Fail: wrong method! Please use one of the following method:")
        for i in ["all", "norm", "t", "historical"]:
            print(i)
        return "Error"

    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import scipy.stats as stats
    import numpy as np

    alphas = np.array(alphas)

    try:
        palphas = [item * 100 for item in alphas]
    except:
        palphas = 100 * alphas

    df_input = np.array(df_input)
    if df_input.ndim > 1:
        if df_input.shape[0] > 1:
            df_input = df_input[:, 0]
        else:
            df_input = df_input[0, :]

    # parametric method with norm distribution
    if method == "norm" or method == "all":
        nloc, nscale = stats.norm.fit(df_input)
        vars = stats.norm.ppf(alphas, loc=nloc, scale=nscale)
        nrvs = stats.norm.rvs(loc=nloc, scale=nscale, size=num_of_simus)
        try:
            ess = [nrvs[nrvs < var].mean() for var in vars]
        except:
            ess = nrvs[nrvs < vars].mean()
        if tell == True or method == "all":
            print("Use Analytical Norm-Distribution model:")
            try:
                for es, alpha in zip(ess, alphas):
                    print("ES {}: \t{} ".format(alpha, es))
            except:
                for es, alpha in zip([ess], [alphas]):
                    print("ES {}: \t{} ".format(alpha, es))
        if method != "all":
            return ess

    # parametric method with t location-scale distribution
    # fit the data with a t location-scale model with MLE
    ## r=loc + scale * T(dof)

    if method == "t" or method == "all":
        tdof, tloc, tscale = stats.t.fit(df_input)
        vars = stats.t.ppf(alphas, df=tdof, loc=tloc, scale=tscale)
        trvs = stats.t.rvs(df=tdof, scale=tscale, size=num_of_simus, loc=tloc)
        try:
            ess = [nrvs[nrvs < var].mean() for var in vars]
        except:
            ess = nrvs[nrvs < vars].mean()

        if tell == True or method == "all":
            print("Use Analytical t location-scale model:")
            try:
                for es, alpha in zip(ess, alphas):
                    print("ES {}: \t{} ".format(alpha, es))
            except:
                for es, alpha in zip([ess], [alphas]):
                    print("ES {}: \t{} ".format(alpha, es))
        if method != "all":
            return ess

    # historical method
    if method == "historical" or method == "all":
        vars = np.percentile(df_input, palphas)
        try:
            ess = [nrvs[nrvs < var].mean() for var in vars]
        except:
            ess = nrvs[nrvs < vars].mean()
        if tell == True or method == "all":
            print("Use Historical Approach:")
            try:
                for es, alpha in zip(ess, alphas):
                    print("ES {}: \t{} ".format(alpha, es))
            except:
                for es, alpha in zip([ess], [alphas]):
                    print("ES {}: \t{} ".format(alpha, es))
        if method != "all":
            return ess


if __name__ == "__main__":

    print("This is my Expected Shortfall module")
    import scipy.stats as stats

    # for calculating ES, we only have 1% or 5% useful data, therefore we want to increase the number of simulations
    df = stats.t.rvs(df=5, scale=2, size=10000, loc=0)

    myes(df, num_of_simus=10000000, alphas=[0.01, 0.05, 0.1])
