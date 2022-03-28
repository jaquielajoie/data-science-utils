import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

def calc_create_ratios(X, feature_names):
    """
    Takes in a numpy array X.
    The function computes the ratios of all features.
    The result is a labeled dataframe.
    The purpose of this function is to postulate what may be important ratio-based structures in a dataset.
    This can be used as input for a NN model.
    Parameters
    ----------
    X: np.array
    i.e. the type of numpy array in the iris dataset. Works with a pandas dataframe as well.
    Returns
    -------
    pd.DataFrame
    This dataframe has the columns labeled with the polynomial and ratio transformations computed.
    This can be later simplified functionally by removed identical columns.
    Sample Usage
    ------------
    import numpy as np
    import pandas as pd
    from sklearn import datasets
    iris = datasets.load_iris()
    X = iris.data[:, :2]
    y = iris.target
    df = calc_create_ratios(X, feature_names=['sepal_length','sepal_width'])
    """
    ratio_idxs = []

    for x1 in range(0,len(feature_names)):
        for x2 in range(0,len(feature_names)):
            if x1 != x2:
                ratio_idxs.append((x1, x2))

    ratio_names = [f'{feature_names[x1]}_by_{feature_names[x2]}'  for x1, x2 in ratio_idxs]

    df = pd.DataFrame(X, columns=feature_names)

    for i, computation in enumerate(ratio_idxs):

        if isinstance(computation, int):
            df[ratio_names[i]] = df.iloc[:, computation]

        if isinstance(computation, tuple):
            df[ratio_names[i]] = df.iloc[:, computation[0]] / df.iloc[:, computation[1]]

    return df

def calc_create_poly_ratios(X, poly):
    """
    Takes in a numpy array X and a fitted instance of sklearn.preprocessing.PolynomialFeatures
    The function computes the polynomial features and ratios of all features including polynomial features and returns
    the result in a labeled dataframe.
    Equivalencies are not removed.
    The purpose of this function is to postulate what may be important ratio-based structures in a dataset.
    This can be used as input for a NN model.
    Parameters
    ----------
    X: np.array
    i.e. the type of numpy array in the iris dataset. Works with a pandas dataframe as well.
    poly: sklearn.preprocessing.PolynomialFeatures
    This must be previously fitted, ideally to degree=2.
    For two features x0 and x1, 23 additional will be created.
    Returns
    -------
    pd.DataFrame
    This dataframe has the columns labeled with the polynomial and ratio transformations computed.
    This can be later simplified functionally by removed identical columns.
    Sample Usage
    ------------
    import numpy as np
    import pandas as pd
    from sklearn import datasets
    from sklearn.preprocessing import PolynomialFeatures
    iris = datasets.load_iris()
    X = iris.data[:, :2]
    y = iris.target
    poly = PolynomialFeatures(degree=2, include_bias=False)
    poly.fit(X)
    df = calc_create_poly_ratios(X, poly)
    """
    poly_feature_names = poly.get_feature_names()

    ratio_idxs = []

    for x1 in range(0,len(poly.get_feature_names())):
        for x2 in range(0,len(poly.get_feature_names())):
            if x1 != x2:
                ratio_idxs.append((x1, x2))

    ratio_names = [f'{poly_feature_names[x1]}_by_{poly_feature_names[x2]}'  for x1, x2 in ratio_idxs]

    all_idxs = [i for i in range(0, len(poly.get_feature_names()))] + ratio_idxs
    all_names = poly.get_feature_names() + ratio_names

    df = pd.DataFrame(poly.transform(X), columns=poly_feature_names)

    for i, computation in enumerate(all_idxs):

        if isinstance(computation, int):
            df[all_names[i]] = df.iloc[:, computation]

        if isinstance(computation, tuple):
            df[all_names[i]] = df.iloc[:, computation[0]] / df.iloc[:, computation[1]]

    return df 
