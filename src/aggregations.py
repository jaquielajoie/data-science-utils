import pandas as pd

def make_count_aggregation(df, grouping_feature, grouped_feature, agg_feature_name):
    """
    Takes in a dataframe. The dataframe must have the grouping_feature and grouped_feature present as columns.
    A count-based aggregation is created for each unique instance of the grouping_feature.
    This count-based aggregation is returned as a new column with the name of agg_feature_name.
    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to create the count-based aggregation for
    grouping_feature: str
        The name of the column in the passed-in dataframe that is used as the Id for aggregation purposes.
    grouped_feature: str
        The feature to be counted per unique instance of grouping_feature.
    agg_feature_name: str
        The name of the new aggregation feature that is added to the original dataframe.
    Returns
    -------
    pd.DataFrame
        The dataframe returned with the new count-based aggregation feature added.
    """
    agg_feature = df.groupby(f'{grouping_feature}')[[f'{grouped_feature}']].nunique()

    df = df.merge(agg_feature, on=f'{grouping_feature}', how='left', suffixes=('', '_agg'))\
        .rename(columns={f'{grouped_feature}_agg': f'{agg_feature_name}'})

    return df

def make_sum_aggregation(df, grouping_feature, grouped_feature, agg_feature_name):
    """
    Takes in a dataframe. The dataframe must have the grouping_feature and grouped_feature present as columns.
    A sum-based aggregation is created for each grouped instance of the grouping_feature.
    This sum-based aggregation is returned as a new column with the name of agg_feature_name.
    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to create the count-based aggregation for
    grouping_feature: str
        The name of the column in the passed-in dataframe that is used as the Id for aggregation purposes.
    grouped_feature: str
        The feature to be summed per grouped instance of grouping_feature.
    agg_feature_name: str
        The name of the new aggregation feature that is added to the original dataframe.
    Returns
    -------
    pd.DataFrame
        The dataframe returned with the new sum-based aggregation feature added.
    """
    agg_feature = df.groupby(f'{grouping_feature}')[[f'{grouped_feature}']].sum()

    df = df.merge(agg_feature, on=f'{grouping_feature}', how='left', suffixes=('', '_agg'))\
        .rename(columns={f'{grouped_feature}_agg': f'{agg_feature_name}'})

    return df

def make_mean_aggregation(df, grouping_feature, grouped_feature, agg_feature_name):
    """
    Takes in a dataframe. The dataframe must have the grouping_feature and grouped_feature present as columns.
    A mean-based aggregation is created for each grouped instance of the grouping_feature.
    This mean-based aggregation is returned as a new column with the name of agg_feature_name.
    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to create the count-based aggregation for
    grouping_feature: str
        The name of the column in the passed-in dataframe that is used as the Id for aggregation purposes.
    grouped_feature: str
        The feature to be averaged per grouped instance of grouping_feature.
    agg_feature_name: str
        The name of the new aggregation feature that is added to the original dataframe.
    Returns
    -------
    pd.DataFrame
        The dataframe returned with the new mean-based aggregation feature added.
    """
    agg_feature = df.groupby(f'{grouping_feature}')[[f'{grouped_feature}']].mean()

    df = df.merge(agg_feature, on=f'{grouping_feature}', how='left', suffixes=('', '_agg'))\
        .rename(columns={f'{grouped_feature}_agg': f'{agg_feature_name}'})

    return df
