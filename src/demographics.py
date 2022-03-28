def birth_generation(birth_year):
    """
    Takes in a birth_year and returns the corresponding generation.
    The earliest corresponding generation is returned.
    Parameters
    ----------
    birth_year: int
        The birth year in question.
    Returns
    -------
    generation: str
        The corresponding generation for the input birth_year
    """
    lost_generation = range(1890, 1915)
    interbellum_generation = range(1901, 1913)
    greatest_generation = range(1910, 1924)
    silent_generation = range(1925, 1945)
    baby_boomers = range(1946, 1964)
    generation_x = range(1965, 1979)
    xennials = range(1975, 1985)
    millennials = range(1980, 1994)
    generation_z = range(1995, 2012)
    generation_alpha = range(2013, 2025)

    if birth_year in lost_generation:
        return 'Lost Generation'

    if birth_year in interbellum_generation:
        return 'Interbellum Generation'

    if birth_year in greatest_generation:
        return 'Greatest Generation'

    if birth_year in silent_generation:
        return 'Silent Generation'

    if birth_year in baby_boomers:
        return 'Baby Boomers'

    if birth_year in generation_x:
        return 'Generation X'

    if birth_year in xennials:
        return 'Xennials'

    if birth_year in millennials:
        return 'Millennials'

    if birth_year in generation_z:
        return 'Generation Z'

    if birth_year in generation_alpha:
        return 'Generation Alpha'

    return 'Unknown'
