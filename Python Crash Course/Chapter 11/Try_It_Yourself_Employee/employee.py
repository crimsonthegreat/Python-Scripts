class Employee:
    """Provide information about an employee"""

    def __init__(self, first, last, salary):
        """Information about the employees name and salary"""
        self.first = first
        self.last = last
        self.salary = salary
        self.full_name = f"{self.first.title()} {self.last.title()}"

    def give_raise(self, given_raise=5000):
        """Give rasie to employee"""
        self.given_raise = given_raise
        if self.given_raise < 5000:
            print("The minimum raise is $5000")
        elif self.given_raise >= 5000:
            self.increased_salary = self.given_raise + self.salary

    def new_annual_salary(self):
        """Get the new annual salary"""
        self.new_salary = self.increased_salary
        print(f"{self.full_name} now has a salary of ${self.new_salary}")