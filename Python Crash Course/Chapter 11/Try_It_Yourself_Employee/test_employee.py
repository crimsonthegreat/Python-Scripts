import pytest

from employee import Employee

@pytest.fixture
def employee():
    first = 'John'
    last = 'Smith'
    salary = 100_000
    employee = Employee(first, last, salary)
    return employee
    
def test_give_custom_raise(employee):
    """Test of custom raise amount"""
    employee.give_raise(10000)
    employee.new_annual_salary()
    assert  employee.new_salary== 110000

def test_give_raise(employee):
    """Test of default raise amount"""
    employee.give_raise()
    employee.new_annual_salary()
    assert  employee.new_salary== 105000