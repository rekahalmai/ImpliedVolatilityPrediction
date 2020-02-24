import collections
import pandas as pd
import numpy as np


def get_subtable(df, strike, duration):
    return df[(df.Strike == strike) & (df.Duration == duration)]


def get_corr(df, strike1, duration1, strike2, duration2):
    """
    Returns the Pearson correlation coefficient between the implied volatity of the time series of two options,
    option 1 and 2 with strike1 and duration1, and strike2 and duration2 respectively.

    :param df: pandas df
    :param strike1: strike value of option 1, int
    :param duration1: duration of option 1, str (one from: ["6M", "1Y", "18M", "2Y", "3Y"])
    :param strike2: strike value of option 2, int
    :param duration2: duration of option 2, str (one from: ["6M", "1Y", "18M", "2Y", "3Y"])
    :return:
    """
    df1 = get_subtable(df, strike1, duration1)
    df2 = get_subtable(df, strike2, duration2)

    return pd.DataFrame(df1.Implied_vol).corrwith(pd.DataFrame(df2.Implied_vol))


def create_corr_table(df):
    """
    Returns a pandas dataframe with Pearson correlation coefficient for each strike-duration pair.

    :param df: pandas df
    :return: pandas df
    """
    DS_tuples = collections.namedtuple('Durations_strikes', ['duration', 'strike'])

    durations = ["6M", "1Y", "18M", "2Y", "3Y"]
    # durations = list(np.unique(df.Duration.values))
    strikes = list(np.unique(df.Strike.values))

    dur_str1 = [DS_tuples(d, s) for d in durations for s in strikes]
    dur_str2 = dur_str1

    duration1, duration2, strike1, strike2, correlations = [], [], [], [], []

    for ds1 in dur_str1:
        for ds2 in dur_str2:
            d1, s1 = ds1[0], ds1[1]
            d2, s2 = ds2[0], ds2[1]

            if d1 < d2:
                if not ((d1 == d2) and (s1 == s2)):
                    corr = get_corr(df, s1, d1, s2, d2)

                    # Save results
                    duration1.append(d1)
                    duration2.append(d2)
                    strike1.append(s1)
                    strike2.append(s2)
                    correlations.append(corr[0])

    corr_dict = {"Duration1": duration1, "Strike1": strike1, "Duration2": duration2, "Strike2": strike2,\
                 "Pearson correlation": correlations}

    return pd.DataFrame(corr_dict)
