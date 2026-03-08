import pizza_mod

pizza_mod.make_pizza(16, 'pepperoni')
pizza_mod.make_pizza(20, 'pepperoni', 'sausage', 'jalapano')

from pizza_mod import make_pizza

make_pizza(12, 'sausage')

from pizza_mod import make_pizza as mp

mp(32, 'extra pepperoni')

import pizza_mod as p

p.make_pizza(12, 'plain cheese')