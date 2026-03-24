from city_functions import city_country

def test_city_country():
    """Does city and country format correctly"""
    formatted_city_country = city_country('phoenix', 'usa')
    assert formatted_city_country == 'Phoenix, USA'

def test_city_country_population():
    """Does city and country with population format correctly"""
    formatted_city_country_pop = city_country('phoenix', 'usa', 100_000_000)
    assert formatted_city_country_pop == 'Phoenix, USA - population 100000000'