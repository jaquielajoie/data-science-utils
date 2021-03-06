import pandas as pd
import numpy as np
from uszipcode import SearchEngine
from uszipcode.model import ZipcodeTypeEnum
from multiprocessing import Pool
import itertools
import csv
import os

def get_location_demographics_from_dict(address, result_limit=None, savepath='', by_city_state=True):
    """
    Takes in a dictionary and returns the lat long based on the maximum amount of detail able to be provided.
    If an address is not able to be found, it will write the city and state to a a csv titled 'bad_address.csv' in the local directory.
    Parameters
    ----------
    address: dict
        {
            'city': str or None,
            'state': str or None,
            'zip': str or None,
        }
        Uses the maximumly detailed address to retunr a lat, long tuple
    result_limit: int
        Limits the number of zip codes returned. Use None for all zip codes.
    savepath: str
        The location to save the city-state pairs that are invalid. This should be a directory and not a file name.
    by_city_state: bool
        Dictates whether the uszipcodes search function should use a city-state pair or a zipcode.
        Both options are set inside the address: dict.
    Returns
    -------
    result: list of SimpeZipcode(s)
        All potential matches for the provided input.
    Examples
    --------
    address = {
        'city': 'New York',
        'state': 'NY',
        'zip': None,
        'country': 'US'
    }
    print(len(get_location_demographics_from_dict(address, result_limit=None))) # There are 101 zipcodes for NYC in the Database.
    >>> 101
    """

    # optimize input address for lookup
    address['city'] = address['city'].title().lstrip().rstrip()
    address['state'] = address['state'].upper().lstrip().rstrip()
    address['zip'] = str(address['zip'])[:5]

    engine = SearchEngine(
        simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.simple
    )

    try:
        if by_city_state:
            result = engine.by_city_and_state(city=address['city'], state=address['state'], zipcode_type=ZipcodeTypeEnum.Standard, returns=result_limit)

        else:
            result = engine.by_zipcode(zipcode=address['zip'])

    except ValueError as v:
            # print('Could not find value for City:', address['city'], 'State:',address['state'], 'skipping instead.')

            # trigger function to drop these records in a CSV function for later analysis
            with open(os.path.abspath(f'{savepath}/value_errors.csv'), 'a', encoding='UTF8', newline='') as f:

                writer = csv.writer(f)
                row = address['row'].to_frame().T.values.flatten().tolist()

                if f.tell()==0:
                    header = ['Zip', 'City', 'State', 'Value Error']
                    header += [i for i in range(0, len(row))]
                    writer.writerow(header)

                data = [address['zip'], address['city'], address['state'], v]
                data += row
                writer.writerow(data)

            return []

    return result

def construct_municipal_area(address, result_limit=None, savepath='', by_city_state=True):
    """
    Takes in an address dictionary and returns a pandas dataframe of all zipcodes that correspond to that municipal area.
    This dataframe can be used to create flexible geographic generalizations.
    Parameters
    ----------
    address: dict
        {
            'city': str or None,
            'state': str or None,
            'zip': str or None,
        }
    result_limit: int or None
        Set to None for the best result. Otherwise limits the number of zipcodes.
    savepath: str
        The location to save the data while run is in-progress. Allows for results to be inspected prior to completion. This should be a directory and not a file name.

    by_city_state: bool
        Dictates whether the uszipcodes search function should use a city-state pair or a zipcode.
        Both options are set inside the address: dict.
    Returns
    -------
    pd.DataFrame
        A pandas dataframe with a variety of metrics by zipcode in accordance to the inputed address.
    Example
    -------
    df = construct_municipal_area(address={
                        'city': 'New York',
                        'state': 'NY'
                        }, result_limit=None)
    print(df.shape)
    >>> (101, 12)
    """
    simple_zipcodes = get_location_demographics_from_dict(address, result_limit=result_limit, savepath=savepath, by_city_state=by_city_state)

    if by_city_state and len(simple_zipcodes) == 0:
        return pd.DataFrame()

    metrics = [
        'zipcode',
        'major_city',
        'lat',
        'lng',
        'timezone',
        'radius_in_miles',
        'population',
        'population_density',
        'housing_units',
        'occupied_housing_units',
        'median_home_value',
        'median_household_income'
    ]

    try:
        if by_city_state:
            df = pd.concat([pd.DataFrame([
                                [
                                    zipcode.zipcode,
                                    zipcode.major_city,
                                    zipcode.lat,
                                    zipcode.lng,
                                    zipcode.timezone,
                                    zipcode.radius_in_miles,
                                    zipcode.population,
                                    zipcode.population_density,
                                    zipcode.housing_units,
                                    zipcode.occupied_housing_units,
                                    zipcode.median_home_value,
                                    zipcode.median_household_income,
                                ]
                            ], columns=metrics) for zipcode in simple_zipcodes
                ], ignore_index=True)
        else:
            df = pd.DataFrame([[
                                    simple_zipcodes.zipcode,
                                    simple_zipcodes.major_city,
                                    simple_zipcodes.lat,
                                    simple_zipcodes.lng,
                                    simple_zipcodes.timezone,
                                    simple_zipcodes.radius_in_miles,
                                    simple_zipcodes.population,
                                    simple_zipcodes.population_density,
                                    simple_zipcodes.housing_units,
                                    simple_zipcodes.occupied_housing_units,
                                    simple_zipcodes.median_home_value,
                                    simple_zipcodes.median_household_income,
                                ]], columns=metrics)
    except AttributeError as a:

        print(a)
        print('Could not resolve:', address['zip'], address['city'], address['state'])
        # trigger function to drop these records in a CSV function for later analysis

        with open(os.path.abspath(f'{savepath}/unresolveable_addresses.csv'), 'a', encoding='UTF8', newline='') as f:

            writer = csv.writer(f)

            if f.tell()==0:
                header = ['Zip', 'City', 'State', 'Attribute Error']
                writer.writerow(header)

            data = [address['zip'], address['city'], address['state'], a]
            writer.writerow(data)

        # For returning a blank dataframe
        df = pd.DataFrame(columns=metrics)

    df = df.fillna(value=0)

    df['radius_in_miles'] = df['radius_in_miles'].astype(int)
    df['population'] = df['population'].astype(int)
    df['population_density'] = df['population_density'].astype(int)
    df['housing_units'] = df['housing_units'].astype(int)
    df['occupied_housing_units'] = df['occupied_housing_units'].astype(int)
    df['median_home_value'] = df['median_home_value'].astype(int)
    df['median_household_income'] = df['median_household_income'].astype(int)

    row = address['row'].to_frame().T # convert series to a pd.DataFrame to append to metric columns

    normalized_row = pd.concat([row] * len(df), ignore_index=True) # repeat row-information for as many zip codes as are returned

    df = pd.concat([df, normalized_row], axis=1, ignore_index=False) # ensure row level details present for every zip code returned

    # Write intermediary step to file
    filename = f'./{savepath}/enriched_addresses.csv'

    with open(filename, 'a', encoding='UTF8', newline='') as f:
        df.to_csv(filename, mode='a', header=f.tell()==0)

    return df

def create_geographic_generalization(address, result_limit=None):
    """
    Returns a pd.DataFrame with the number of zipcodes and mean, std, min, and max statistics for a variety of metrics.
    Parameters
    ----------
    address: dict
        {
            'city': str or None,
            'state': str or None,
            'zip': str or None,
        }
    result_limit: int or None
        Set to None for best results.
    Returns
    -------
    pd.DataFrame
        The dataframe is labeled with the inputed along with the statistics.
    Examples
    --------
    df = create_geographic_generalization(address={
                                'city': 'New York',
                                'state': 'NY',
                                }, result_limit=None)
    df.shape
    >>> (5, 11)
    """
    df = construct_municipal_area(address={
                            'city': 'New York',
                            'state': 'NY',
                            }, result_limit=result_limit)

    df = df.describe().loc[['count', 'mean', 'std', 'min', 'max']]
    df['city'] = address['city']
    df['state'] = address['state']

    return df

def _apply_construct_municipal_area(df, savepath, by_city_state):
    """
    This is a helper function to parrellilize the processing of contruct_municipal_area accross multiple cores.
    This function should be called from within a Pool.map() function.

    The rest of the row (for reference purposes) is passed in as address['row']
    """
    df.apply(lambda row: construct_municipal_area(address={'city': row['City'], 'state': row['State'], 'zip': row['Zip'], 'row': row}, savepath=savepath, by_city_state=by_city_state), axis=1)

    return  # can process roughly 5K per hour per core

def parallel_construct_municipal_area(df, n_cores=6, savepath='', by_city_state=True):
    """
    This function parrellel processes a dataframe running the _apply_construct_municipal_area across multiple cores.
    Pool management occurs in this function.

    by_city_state=False executes roughly ~3x faster than by_city_state=True
    by_city_state=False can process ~5k observations per core per hour.

    Zip codes must by in 5 digit format.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe that will have the _apply_construct_municipal_area applied to it.
    n_cores: int
        The number of cores on your machine (for max speed).
    savepath: str
        The location where bad_addresses.csv and enriched_addresses_in_progress.csv will be stored. This should be a directory, and not a file name.
    by_city_state: bool
        Dictates whether the uszipcodes search function should use a city-state pair or a zipcode.
        Both options are set inside the address: dict.
    Returns
    -------
    df: pd.DataFrame
        For the addresses able to be found, enriched details are returned for each city, state combo.
        Every zipcode in the city, state combo is returned in its own row with the following columns present:
            'zipcode',
            'major_city',
            'lat',
            'lng',
            'timezone',
            'radius_in_miles',
            'population',
            'population_density',
            'housing_units',
            'occupied_housing_units',
            'median_home_value',
            'median_household_income'
    Example
    -------
    import os

    relative_save_path = 'runs/run_1'
    os.mkdir(os.path.abspath(relative_save_path))

    # Impute NoneType zipcodes to 00501 -- no one lives here (special IRS zip code)
    df_city_state['Zip'] = df_city_state['Zip'].fillna('00501')

    # Truncate 9 digit zipcodes to 5 digits
    df_city_state['Zip'] = df_city_state['Zip'].str[:5]

    parrallelize_construct_municipal_area(df_city_state.iloc[:,:], n_cores=4, savepath=relative_save_path, by_city_state=False)
    """

    df_split = np.array_split(df, n_cores)

    try:

        with Pool(processes=n_cores) as pool:

            pool.starmap(_apply_construct_municipal_area, zip(df_split, itertools.repeat(savepath), itertools.repeat(by_city_state)))

        print('parrallelize_construct_municipal_area() has completed.')

    except AttributeError as a:
        print(a)

        for i, df in enumerate(df_split):

            print(f'df_split ({i}): ', df)

        print('savepath:', savepath)
        print('by_city_state:', by_city_state)

        print('Please try imputing the missing values and then run again.')

    return
