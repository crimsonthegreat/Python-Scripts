from car import ElectricCar

my_new_leaf = ElectricCar('nissan', 'leaf', 2024)
print(my_new_leaf.get_descriptive_name())
my_new_leaf.battery.describe_battery()
my_new_leaf.battery.get_range()