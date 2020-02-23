import matplotlib.pyplot as plt
import numpy as np

def single_graph(df, x_col, y_col):
    """
    Plots the y_col as a function of the x_col

    :param df: pandas df
    :param x_col: str (col of df)
    :param y_col: str (col of df)
    :return: None
    """
    title = f'{x_col} vs {y_col}'
    plt.figure(figsize=(14, 8))

    params = {"text.color": "midnightblue",
              "xtick.color": "black",
              "ytick.color": "black"}
    plt.rcParams.update(params)

    plt.plot(df[x_col], df[y_col], 'midnightblue')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)


    plt.show()
    return


def graph_df_strike_duration_selection(df, duration, strike, x_col, y_col):
    """
    Plots for different strike and duration values

    :param df: pandas df
    :param duration: duration of the option ("6M", "1Y", "18M", "2Y", "3Y")
    :param strike: strike of the option (30, 40, 60, 80, 90, 100, 110, 120, 140)
    :param x_col: str (col of df)
    :param y_col: str (col of df)
    :return: None
    """

    temp_df = df[(df.Duration == duration) & (df.Strike == strike)]
    single_graph(temp_df, x_col, y_col)

    return


def plot_different_strike_values(df, duration="6M", x_col="Dates", y_col="Real_implied_vol"):
    """
    Plots the x_col and y_col for different strike values

    :param df: pandas df
    :param duration: duration of the option ("6M", "1Y", "18M", "2Y", "3Y")
    :param x_col: will be the x axis (should be "Dates")
    :param y_col: will be the y axis
    :return: None
    """
    strikes = np.unique(df.Strike)
    palette = plt.get_cmap('Set1')

    plt.figure(figsize=(14, 8))

    params = {"text.color": "black",
              "xtick.color": "black",
              "ytick.color": "black"}
    plt.rcParams.update(params)

    title = f'{x_col} vs {y_col} for different strike values and {duration} duration'
    col_count = 0

    for s in strikes:
        temp_df = df[(df["Duration"] == duration) & (df["Strike"] == s)]
        plt.plot(temp_df[x_col], temp_df[y_col], marker='', color=palette(col_count), \
                 linewidth=1, alpha=1, label=s)
        col_count += 1
    plt.legend(ncol=2, title='Strike', title_fontsize=12)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title, fontsize=14)
    plt.show()

    return


def plot_different_duration_values(df, strike=30, x_col="Dates", y_col="Real_implied_vol"):
    """
    Plots the x_col and y_col for different duration values

    :param df: pandas df
    :param strike: strike of the option (30, 40, 60, 80, 90, 100, 110, 120, 140)
    :param x_col: will be the x axis (should be "Dates")
    :param y_col: will be the y axis
    :return: None
    """
    durations = np.unique(df.Duration)
    palette = plt.get_cmap('Set1')

    plt.figure(figsize=(14, 8))

    params = {"text.color": "black",
              "xtick.color": "black",
              "ytick.color": "black"}
    plt.rcParams.update(params)

    title = f'{x_col} vs {y_col} for different duration values and {strike} strike'
    col_count = 0

    for d in durations:
        temp_df = df[(df["Duration"] == d) & (df["Strike"] == strike)]
        plt.plot(temp_df[x_col], temp_df[y_col], marker='', color=palette(col_count), \
                 linewidth=1, alpha=1, label=d)
        col_count += 1
    plt.legend(ncol=2, title='Duration', title_fontsize=12)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title, fontsize=14)
    plt.show()

    return