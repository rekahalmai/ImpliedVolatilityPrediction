import os
import sys
import logging
import pandas as pd

file = sys.argv[1]
logger = logging.getLogger()


def open_and_transform_csv(file):
    df = pd.read_excel(file, header=[2, 3], parse_dates=True)
    cols = df.columns

    df_total = pd.DataFrame()
    df_one_col = pd.DataFrame()

    if 'weekly' in str(file):
        dates_spots = pd.DataFrame(df[[('Unnamed: 0_level_0', 'Dates'), \
                                       ('Unnamed: 1_level_0', 'Spot t'), \
                                       ('Unnamed: 2_level_0', 'Spot t-5')]])
    else:
        dates_spots = pd.DataFrame(df[[('Unnamed: 0_level_0', 'Dates'), \
                                       ('Unnamed: 1_level_0', 'Spot t'), \
                                       ('Unnamed: 2_level_0', 'Spot t-1')]])

    dates_spots.columns = [f'{j}' for i, j in dates_spots.columns]

    for i in range(3, 47):
        duration, strike = cols[i]
        logger.info(f'Treating column duration: {duration}, strike: {strike}')
        df_one_col, df_one_col["Implied_vol"] = dates_spots, pd.DataFrame(df.iloc[:, i])
        df_one_col['Duration'], df_one_col['Strike'] = duration, strike
        df_one_col["Real_implied_vol"] = df.iloc[:, i + 51]
        df_total = pd.concat([df_total, df_one_col])

    df_total = df_total.dropna()
    logger.info(df_total.isnull().sum())

    return df_total


def preprocess_df(df):
    # Changing the duration to day equivalent
    duration_value_map = {'18M': 1.5, '1Y': 1, '2Y': 2, '3Y': 3, '6M': 0.5}
    df['Duration_days'] = df.Duration.map(duration_value_map)

    # Changing the date variable to years, months and days
    df['Year'], df['Month'], df['Day'] = df.Dates.map(lambda x: x.year), \
                                         df.Dates.map(lambda x: x.month), df.Dates.map(lambda x: x.day)
    df['Weekday'] = df.Dates.map(lambda x: x.weekday())

    return df


def main():
    file = sys.argv[1]
    logger = logging.getLogger()