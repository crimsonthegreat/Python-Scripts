from car import Car
from electric_car import ElectricCar

my_mustang = Car('ford', 'mustang', 2026)
print(my_mustang.get_descriptive_name())
my_leaf = ElectricCar('nissan', 'leaf', 2024)
print(my_leaf.get_descriptive_name())


import car
import electric_car

my_mustang = car.Car('ford', 'mustang', 2026)
print(my_mustang.get_descriptive_name())
my_leaf = electric_car.ElectricCar('nissan', 'leaf', 2024)
print(my_leaf.get_descriptive_name())

from electric_car import ElectricCar as EC

my_leaf = EC('nissan', 'leaf', 2024)
print(my_leaf.get_descriptive_name())