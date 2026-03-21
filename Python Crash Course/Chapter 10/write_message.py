from pathlib import Path

path = Path('programming.txt')
path.write_text("I love programming!")
initial_msg = path.read_text()
print(initial_msg)

contents = "I love programming!\n"
contents += "I love creating new games.\n"
contents += "I also love working with data.\n"

path.write_text(contents)
second_msg = path.read_text()
print(second_msg)