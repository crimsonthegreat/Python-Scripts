#Inital variable list places
places = []
#Append Places to the list
places.append('Germany')
places.append('New Zealand')
places.append('Italy')
places.append('South Korea')
places.append('Japan')
#Print places in original order
print(places)

#Print places in sorted order
print(f'\n{sorted(places)}')
print(places)

#Print places in reverse sorted order
print(f'\n{sorted(places, reverse=True)}')
print(places)

#Print in reverse order
places.reverse()
print(f'\n{places}')
places.reverse()
print(places)

#Sort places in alphabetical order
places.sort()
print(f'\n{places}')
places.sort(reverse=True)
print(places)

#Length of places list
print(len(places))