# 8.6
def city_country(city_name, country):
    """Get city and country information and dispaly it"""
    cc = f"{city_name}, {country}"
    return cc.title()

place = city_country('Munich', 'Germany')
print(place)

place = city_country('Brussels', 'Belgium')
print(place)

place = city_country('London', 'England')
print(place)

# 8.7
def make_album(artist_name, album_title, num_songs=None):
    """Create dictionary for an artist and their ablum"""
    music = {'artist' : artist_name, 'album' : album_title}
    if num_songs:
        music['num_songs'] = num_songs
    return music

studio_record = make_album('Five Finger Death Punch', 'White Knuckle')
print(studio_record)

studio_record = make_album('Pink Floyd', 'The Wall', 26)
print(studio_record)

studio_record = make_album('AC/DC', 'Back in Black', 10)
print(studio_record)

# 8.8
def make_album(artist_name, album_title, num_songs=None):
    """Create dictionary for an artist and their ablum"""
    music = {'artist' : artist_name, 'album' : album_title, 'num_songs' : num_songs}
    return music

while True:
    print("\nPlease enter the information about your favorite band:")
    print("(Enter 'q' to quite at any point)")
    artist = input("Artist name: ")
    if artist == 'q':
        break 

    album = input("Album name: ")
    if album == 'q':
        break

    songs = input("(Optional) Number of songs: ")
    if songs == 'q':
        break

    studio_record = make_album(artist, album, songs)
    print(studio_record)
