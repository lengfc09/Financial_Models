def myhist(df_input, bins=30):
    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import scipy.stats as stats
    import numpy as np

    df_input = np.array(df_input)
    if df_input.ndim > 1:
        if df_input.shape[0] > 1:
            df_input = df_input[:, 0]
        else:
            df_input = df_input[0, :]

    style.use("ggplot")
    plt.rcParams["figure.figsize"] = (6, 4)
    plt.figure(dpi=100)
    heightofbins, aa, bb = plt.hist(df_input, bins)
    mu = df_input.mean()
    std = df_input.std()
    lowb = df_input.min()
    upb = df_input.max()

    # can use stats.norm.fit to get the std, mu
    # nloc,nscale=stats.norm.fit(df_input)

    # fit the data with a t location-scale model with MLE
    ## r=loc + scale * T(dof)

    tdof, tloc, tscale = stats.t.fit(df_input)

    # Change the shape of PDF to match the hist
    ## both norm and t distribution pdf are multiplied by a same number

    ### norm distribution
    xx = stats.norm.pdf(np.linspace(lowb - std, upb + std, 1000), loc=mu, scale=std)
    xx = xx * np.max(heightofbins) / stats.t.pdf(mu, df=tdof, loc=tloc, scale=tscale)
    plt.plot(np.linspace(lowb - std, upb + std, 1000), xx)

    ### rescaled t distribution
    y = stats.t.pdf(
        np.linspace(lowb - std, upb + std, 1000), df=tdof, loc=tloc, scale=tscale
    )
    y = y * np.max(heightofbins) / stats.t.pdf(mu, df=tdof, loc=tloc, scale=tscale)
    plt.plot(np.linspace(lowb - std, upb + std, 1000), y)

    plt.legend(["Normal PDF", "Rescaled t Distribution", "Sample Distribution"])

    ### plot the sample kurtosis and skewness
    kur = stats.kurtosis(df_input)
    skew = stats.skew(df_input)
    x = mu + std
    y = 0.5 * np.max(heightofbins)
    plt.text(x, y, "Skewness:{:.2f},Kurtosis:{:.2f}".format(skew, kur))
    plt.show()


def myvar(df_input, alphas=[0.01, 0.05], method="all", tell=True):
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
    # Analytic Approach
    if method == "norm" or method == "all":
        nloc, nscale = stats.norm.fit(df_input)
        vars = stats.norm.ppf(alphas, loc=nloc, scale=nscale)
        if tell == True or method == "all":
            print("Use Norm-Distribution model:")
            try:
                for var, alpha in zip(vars, alphas):
                    print("Var {}: \t{} ".format(alpha, var))
            except:
                for var, alpha in zip([vars], [alphas]):
                    print("Var {}: \t{} ".format(alpha, var))

        if method != "all":
            return vars

    # parametric method with t location-scale distribution
    # fit the data with a t location-scale model with MLE
    ## r=loc + scale * T(dof)

    if method == "t" or method == "all":
        tdof, tloc, tscale = stats.t.fit(df_input)
        vars = stats.t.ppf(alphas, df=tdof, loc=tloc, scale=tscale)
        if tell == True or method == "all":
            print("Use t location-scale model:")
            try:
                for var, alpha in zip(vars, alphas):
                    print("Var {}: \t{} ".format(alpha, var))
            except:
                for var, alpha in zip([vars], [alphas]):
                    print("Var {}: \t{} ".format(alpha, var))

        if method != "all":
            return vars

    # historical method
    if method == "historical" or method == "all":
        vars = np.percentile(df_input, palphas)
        if tell == True or method == "all":
            print("Use Historical Approach:")
            try:
                for var, alpha in zip(vars, alphas):
                    print("Var {}: \t{} ".format(alpha, var))
            except:
                for var, alpha in zip([vars], [alphas]):
                    print("Var {}: \t{} ".format(alpha, var))

        if method != "all":
            return vars


if __name__ == "__main__":

    print("This is my first module")

    from WindPy import w
    import scipy.stats as stats

    w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒

    print("WindPy是否已经登录成功:{}".format(w.isconnected()))  # 判断WindPy是否已经登录成功

    eroc, df = w.wsd("USDCNY.EX", "close", "2010-01-01", "2020-12-28", usedf=True)
    myhist(df.diff().dropna(), bins=100)
    myvar(df.diff().dropna(), method="t", tell=True)
    import pandas as pd

    df.index = pd.to_datetime(df.index)
    for i in range(2015, 2021):
        print("For year {}:".format(i))
        myvar(-df[df.index.year == i].diff().dropna(), method="t", tell=True)
        parameters = stats.t.fit(-df[df.index.year == i].diff().dropna())
        print("DF={}\t Loc={}\t Scale={}".format(*parameters))
        print("The stats are:")
        statistics = stats.t.stats(*parameters, moments="mvsk")
        print("Mean={}\t Variance={}\t Skew={}\t Kurtosis={}".format(*statistics))
        print("-------------------------------------------")
