from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import linspace
from scipy.stats import norm


def test_stationarity(timeseries):
    """
    Augmented Dickey-Fuller test for time series

    :param timeseries: pd.Series (if given as a col of a dataframe use df["col"].values
    :return: None
    """
    print("Results of ADF test: ")
    df_test = adfuller(timeseries, autolag="AIC")
    df = pd.Series(df_test[0:4],
                   index=["Test statistics", "P-value", "Number of lags used", "Number of observations used"])

    print(df)


def acf_pacf_plots(df):
    """
    Boucle on the df and plots the ACF and PACF plots for each strike-maturity.

    :param df:
    :return:
    """
    strikes = [40, 60, 80, 90, 100, 110, 120]
    durations = ['6M', '1Y', '18M', '2Y', '3Y']

    for s in strikes:
        for d in durations:
            df_temp = df[(df.Strike == s) & (df.Duration == d)]

            print(f"Strike: {s}, Maturity: {d}")

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 8))
            plot_acf(df_temp["Change_in_implied_vol"].values, lags=100, ax=ax1, \
                     title=f"Autocorrelation Function for Strike: {s}, Maturity: {d}")
            plot_pacf(df_temp["Change_in_implied_vol"].values, lags=100, ax=ax2, \
                      title=f"Partial Autocorrelation Function for Strike: {s}, Maturity: {d}")
            plt.show()

    return


def rolling_mean_std(df, col, window, s, d):
    """
    Plots rolling averages and rolling std for col in df with window size window.

    :param df: pd df
    :param col: str, name of col to plot
    :param window: int, size of window
    :param s: strike, one from the list [40, 60, 80, 90, 100, 110, 120]
    :param d: str, maturity, one from ['6M', '1Y', '18M', '2Y', '3Y']
    :return: None
    """
    ts = pd.Series(df[col].values, index=pd.date_range(start=df.Dates.values.min(), \
                                                       periods=df.shape[0], freq="D"))

    ts_mean = ts.rolling(window).mean()
    ts_std = ts.rolling(window).std()

    plt.figure(figsize=(20, 8))
    plt.plot(ts, color="orange", label="Original ts")
    plt.plot(ts_mean, color="darkblue", label="Rolling mean ts")
    plt.plot(ts_std, color="darkred", label="Rolling std ts")
    plt.legend(loc="best")
    plt.title(f"Original {col}, rolling mean and rolling std with window of {window} for strike: {s} and maturity {d}")
    plt.show()

    return


def plot_rolling_averages(df, col, window):
    """
    Plots rolling averages and std for all strike-maturity options in the df.

    :param df: pd df
    :param col: str, name of col to plot
    :param window: int, window size
    :return: None
    """
    strikes = [40, 60, 80, 90, 100, 110, 120]
    durations = ['6M', '1Y', '18M', '2Y', '3Y']

    for s in strikes:
        for d in durations:
            df_temp = df[(df.Strike == s) & (df.Duration == d)]
            print(f"Rolling mean and std for maturity: {d} and strike: {s}")

            rolling_mean_std(df_temp, col, window, s, d)

    return


def ewma(df, col, alpha, s, d):
    """
    Plots the Exponentially Weighted Moving Average of a df col column.

    :param df: pd df
    :param col: str, name of col to plot
    :param alpha: float between 0 and 1
    :param s: strike, one from the list [40, 60, 80, 90, 100, 110, 120]
    :param d: str, maturity, one from ['6M', '1Y', '18M', '2Y', '3Y']
    :return: None
    """
    ts = pd.Series(df[col].values, index=pd.date_range(start=df.Dates.values.min(), \
                                                       periods=df.shape[0], freq="D"))

    ts_mean = ts.ewm(alpha=alpha).mean()
    ts_std = ts.ewm(alpha=alpha).std()

    plt.figure(figsize=(20, 8))
    plt.plot(ts, color="orange", label="Original ts")
    plt.plot(ts_mean, color="darkblue", label="Ewma ts")
    plt.plot(ts_std, color="darkred", label="Ewma std ts")
    plt.legend(loc="best")
    plt.title(f"Original {col}, ewma and std with alpha of {alpha} for strike: {s} and maturity {d}")
    plt.show()

    return


def plot_ewmas(df, col, alpha):
    """
    Plots ewmas and std for all strike-maturity options in the df.

    :param df: pd df
    :param col: str, name of col to plot
    :param alpha: float between 0 and 1
    :return: None
    """
    strikes = [40, 60, 80, 90, 100, 110, 120]
    durations = ['6M', '1Y', '18M', '2Y', '3Y']

    for s in strikes:
        for d in durations:
            df_temp = df[(df.Strike == s) & (df.Duration == d)]
            print(f"Rolling mean and std for maturity: {d} and strike: {s}")

            ewma(df_temp, col, alpha, s, d)

    return





def residual_histogram(residuals):
    """
    Plots the residuals and a normal distribution with the residuals mean and variance.

    :param residuals: pd Series
    :return: None
    """
    fig = plt.figure(figsize=(20, 8))

    plt.hist(residuals, bins="auto", density=True, rwidth=0.5, label="Residuals")
    mean_resid, std_resid = norm.fit(residuals)
    x_min, x_max = plt.xlim()

    curve_length = linspace(x_min, x_max, 100)
    bell_curve = norm.pdf(curve_length, mean_resid, std_resid)
    plt.plot(curve_length, bell_curve, "red", linewidth=2)
    plt.grid(axis="y", alpha=0.2)
    plt.xlabel("Residuals")
    plt.ylabel("Density")
    plt.title(f"Residuals vs Normal distribution with {round(mean_resid, 3)} mean and {round(std_resid, 3)} std")

    plt.show()

    return



def plot_acf_residuals(data, lags):
    """
    Plots the ACF plot for data with lags number of lags.
    :param data: pd.Series
    :param lags: int
    :return: None
    """
    print(f"The residual mean: {np.mean(data)}") # Result is close to 0, it's good.

    fig = plt.figure(figsize=(20, 8))
    ax1 = fig.add_subplot(211)
    fig = plot_acf(data, lags=lags, ax=ax1)
    plt.show()

    return