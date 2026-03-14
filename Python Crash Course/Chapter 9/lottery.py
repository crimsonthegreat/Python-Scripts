from random import choice

class Lottery:
    """Model the lottery"""

    def __init__(self):
        """Initilize the lottery"""
        self.lottery = ['a', 'b', 'c', 'd', 'e']
        numbers = range(0, 10)
        for number in numbers:
            self.lottery.append(number)

    def lottery_selection(self):
        """Select the winning lotter characters"""
        characters = 0
        self.lottery_list = []

        while characters < 4:
            chosen = choice(self.lottery)
            characters += 1
            self.lottery_list.append(str(chosen))
        
        print(self.lottery_list)

    def my_ticket(self):
        """My ticket numbers"""
        self.ticket = []
        number = 1

        if number == 1:
            suffix = "st"
        elif number == 2:
            suffix = "nd"
        elif number == 3:
            suffix = "rd"
        else:
            suffix = "th"

        print("Valid characters are 1-9 and a-e")
        while number < 5:
            char = input(f"Please enter your {number}{suffix} for your winning "
                            "lottery ticket: ")
            self.ticket.append(char)
            number += 1

    def check_winnings(self):
        """Check to see if your ticket wins"""
        count = 0

        while self.lottery_list != self.ticket:
            print("The numbers do not match.")
            count += 1
            print(f"The number of tries is: {count}")
            print("The winning lottery characters are:")
            self.lottery_selection()
        
        print(f"Your numbers matched! Congradulations, it took {count} "
              "tries to win.")
