from name_functions import get_formatted_name

def test_first_last_name():
    """Do names like 'Janis Joplin' work?"""
    formatted_name = get_formatted_name('janis', 'joplin')
    assert formatted_name == 'Janis Joplin'

def test_first_last_middle_name():
    """Do names like 'Wolfgang Amadeus Motzart' work?"""
    formatted_name = get_formatted_name('wolfgang', 'motzart', 'amadeus')
    assert formatted_name == 'Wolfgang Amadeus Motzart'