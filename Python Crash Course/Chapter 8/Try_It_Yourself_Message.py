# 8.1
def message():
    """Display a message about what I am learning"""
    print("This chapter is teaching me about functions"
          " and the way they operate in Python!")

# 8.2
def favorite_books(book):
    """Display favorite book"""
    print(f"My favorite book is {book.title()}")

message()
favorite_books('Python Crash Course')