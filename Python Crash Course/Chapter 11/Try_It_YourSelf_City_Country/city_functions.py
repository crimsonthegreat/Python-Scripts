def city_country(city, country, population=0):
    """Formst city and country names"""
    if population > 0:
        if country == 'usa' or country == 'USA':
            formatted_city = f"{city.title()}, {country.upper()} - population "
            formatted_city += f"{population}"
        else:
            formatted_city = f"{city.title()}, {country.title()} - population "
            formatted_city += f"{population}"
    else:
        if country == 'usa' or country == 'USA':
            formatted_city = f"{city.title()}, {country.upper()}"
        else:
            formatted_city = f"{city.title()}, {country.title()}"
    return formatted_city