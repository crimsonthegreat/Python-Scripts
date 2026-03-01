#List of Bicycles
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles)
#Print the first item of the list
print(bicycles[0])
#Print the first item of the list in title case
print(bicycles[0].title())
#Print the second item of the list in title case
print(bicycles[1].title())
#print the fourth item of the list in title case
print(bicycles[3].title())
#print the last item of the list in title case
print(bicycles[-1].title())

message = f'My first bicycle was a {bicycles[0].title()}.'

print(message)