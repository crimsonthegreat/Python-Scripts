#Initial list of outdoors locations
outdoors = []

#append outdoors locations to the list
print('Beginning the list of outdoors locations:')
outdoors.append('Mountains')
print(outdoors)

#insert outdoors locations to the list
outdoors.insert(0, 'Rivers')
print(outdoors)

#Append additional outdoors locations to the list
outdoors.append('Lakes')
outdoors.append('Beaches')
outdoors.append('Forests')
outdoors.append('Deserts')
outdoors.append('Canyons')
print(outdoors)
print(f'Length of the outdoors list: {len(outdoors)}')

#Print list in reverse order
outdoors.reverse()
print(f'\n{outdoors}')

#Reverse the order to original
outdoors.reverse()
print(outdoors)

#Print outdoors locations in sorted order
print(f'\n{sorted(outdoors)}')

#Print outdoors locations in reverse sorted order
print(f'\n{sorted(outdoors, reverse=True)}')

#Sort the list of outdoors locations in alphabetical order
outdoors.sort()
print(f'\n{outdoors}')

#sort the list of outdoors locations in reverse alphabetical order
outdoors.sort(reverse=True)
print(f'\n{outdoors}')

#Remove places from the list
do_not_visit = input('Which outdoors location do you not want to visit? ')
outdoors.remove(do_not_visit)

#Pop places from the list
no_my_style = outdoors.pop()
print(f'\n{no_my_style} are not my ideal outdoors location.')
print(outdoors)

#Delete outdoors locations
del outdoors[0]
del outdoors[1]
del outdoors[-1]
print(f'\nThe remaining {len(outdoors)} places that I want to visit are:')
print(f'{outdoors[0]} and {outdoors[1]}.')

