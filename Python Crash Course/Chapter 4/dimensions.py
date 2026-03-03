#Tuple dimensions
dimensions = (200, 90)
print(dimensions[0])
print(dimensions[1])

#For loop tuple dimensions
dimensions = (200, 90)
for dimension in dimensions:
    print(dimension)

#Chaning a tuple
dimensions = (200, 90)
print("Original Dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 180)
print("New dimensions:")
for dimension in dimensions:
    print(dimension)

#Unable to reassign a tuple value
dimensions = (200, 90)
dimensions[0] = 250
