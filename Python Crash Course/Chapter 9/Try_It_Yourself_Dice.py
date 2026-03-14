from dice import Die
from lottery import Lottery

# 9.13
die_six = Die()
die_ten = Die(10)
die_twenty = Die(20)

print(f"\nRolling the {die_six.sides}-sided die 10 times")
die_six.roll_die()
die_six.reset_rolls()
 
print(f"\nRolling the {die_ten.sides} sided die 10 times")
die_ten.roll_die()
die_ten.reset_rolls()

print(f"\nRolling the {die_twenty.sides} sided die 10 times")
die_twenty.roll_die()
die_twenty.reset_rolls()

# 9.14
lotto = Lottery()
lotto.lottery_selection()
lotto.my_ticket()
lotto.check_winnings()