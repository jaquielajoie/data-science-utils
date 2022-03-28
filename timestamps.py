import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

def process_timestamps(df):
    """
    Takes in a dataframe with timestamps and returns a myriad of features for all timestamps present.
    The original dataframe is returned with these new features and the timestamps removed.
    This is useful for algorithms that cannot interpret raw timestamps.
    Parameters
    ----------
    df: pd.DataFrame
        A pandas dataframe with timestamp columns.
    Returns
    -------
    pd.DataFrame
        The original dataframe with the new timestamp-derived features and the original timestamp columns removed.
        New Features:
            - Week number in the year (string)
            - Weekday value (string)
            - Year (string)
            - Month (string)
            - Day (string)
            - Week of month (string)
            - Hour(string)
            - Minute (string)
            - Second (string)
            - During Morning (bool)
            - During Afternnon (bool)
            - During Evening (bool)
            - During Night (bool)
            - Near [within 2 weeks of] a US Federal Holiday (bool)
        String objects were used for number values that are better interpretted as categories.
        Week 1 and week 52 are adjacent – a numeric interpretation would not facillitate this interpretation.
    """

    for col in df.select_dtypes(include=np.datetime64).columns:
        t = pd.DataFrame(df[col].apply(lambda x: x.isocalendar()).tolist(), columns=['year','week_num','weekday'], index=df[col].apply(lambda x: x.isocalendar()).index)
        df[f'{col}_week_num'] = t['week_num'].astype(str)
        df[f'{col}_weekday'] = t['weekday'].astype(str)

        df[f'{col}_year'] = df[col].dt.year.astype(str)
        df[f'{col}_month'] = df[col].dt.month.astype(str)
        df[f'{col}_day'] = df[col].dt.day.astype(str)
        df[f'{col}_week_of_month'] = ((df[col].dt.day // 7) + 1).astype(str)

        df[f'{col}_hour'] = df[col].dt.hour.astype(str)
        df[f'{col}_minute'] = df[col].dt.minute.astype(str)
        df[f'{col}_second'] = df[col].dt.second.astype(str)

        morning = (6,7,8,9,10,11)
        afternoon = (12,13,14,15,16,17)
        evening = (18,19,20,21,22,23)
        night = (0,1,2,3,4,5)

        df[f'{col}_during_morning'] = df[col].isin(morning)
        df[f'{col}_during_afternoon'] = df[col].isin(afternoon)
        df[f'{col}_during_evening'] = df[col].isin(evening)
        df[f'{col}_during_night'] = df[col].isin(night)

        cal = USFederalHolidayCalendar()

        holidays = cal.holidays(start=df[col].min(), end=df[col].max())
        holiday_weeks = holidays

        for h in holidays:
            h_week = pd.date_range(start=h - pd.Timedelta(days=7), end=h + pd.Timedelta(days=7)) # Naively takes 7 days before and after holiday
            holiday_weeks = holiday_weeks.append(h_week)

        df[f'{col}_near_holiday'] = df[col].dt.date.isin(holiday_weeks)

    df = df.select_dtypes(exclude=np.datetime64)

    return df
