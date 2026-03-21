from pathlib import Path
import json

# 10.12 ask for user's favorite number and output it
path = Path('favorite_number.json')

# If the file exists tell the user their favorite number
if path.exists():
    contents = path.read_text()
    favorite_number = json.loads(contents)
    print(f"I know your favorite number is {favorite_number}!")
# If the file does not exist, as the user their favorite number
# Tell the user you will remember the number in the future
else:
    favorite_number = input("What is your favorite number? ")
    contents = json.dumps(favorite_number)
    path.write_text(contents)
    print(f"I will remember you favorite number is {favorite_number} "
          "in the future!")