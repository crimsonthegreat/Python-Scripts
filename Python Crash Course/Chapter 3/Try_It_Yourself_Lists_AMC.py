#Inital dinner guest list
dinner_guests = ['reddog', 'muchow', 'zaq', 'slick']
print(f'{dinner_guests[0].title()} has been invited to dinner.')
print(f'{dinner_guests[1].title()} has been invited to dinner.')
print(f'{dinner_guests[2].title()} has been invited to dinner.')
print(f'{dinner_guests[3].title()} has been invited to dinner.')

#Dinner guest cannot make it
print(f'\n{dinner_guests[-1].title()} cannot make it to dinner.')
#Change dinner guest list
dinner_guests[-1] = 'Hammerhead'
print(f'\n{dinner_guests[-1].title()} has been invited to dinner.')

#Bigger tasble found
print('\nA bigger tables has been found and more guests can be invited to dinner.')
#Add new guests to the list
dinner_guests.insert(0, 'Kevlar')
dinner_guests.insert(3, 'Nick')
dinner_guests.append('Charlie')
print(f'\n{dinner_guests[0].title()} has been invited to dinner.')
print(f'{dinner_guests[3].title()} has been invited to dinner.')
print(f'{dinner_guests[-1].title()} has been invited to dinner.')

#Shrink the guest list
print('\nThe new table will not arrive in time and there is only room for 2 guests.')
#Remove guests from the list
remove_guest_1 = dinner_guests.pop(0)
print(f'\n{remove_guest_1.title()} has been removed from the guest list.')
remove_guest_2 = dinner_guests.pop(2)
print(f'{remove_guest_2.title()} has been removed from the guest list.')
remove_guest_3 = dinner_guests.pop(-1)
print(f'{remove_guest_3.title()} has been removed from the guest list.')
remove_guest_4 = dinner_guests.pop(-1)
print(f'{remove_guest_4.title()} has been removed from the guest list.')
remove_guest_5 = dinner_guests.pop(-1)
print(f'{remove_guest_5.title()} has been removed from the guest list.')
#Print the guests that are still invited
print(f'\n{dinner_guests[0].title()} is still invited to dinner.')
print(f'{dinner_guests[1].title()} is still invited to dinner.')

#Empty the list
del dinner_guests[0]
del dinner_guests[0]
print(dinner_guests)