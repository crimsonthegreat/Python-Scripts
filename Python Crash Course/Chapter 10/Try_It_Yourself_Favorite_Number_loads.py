from pathlib import Path
import json

# 10.11 Tell the user you know their favorite number and display it
path = Path('favorite_number.json')
contents = path.read_text()
favorite_number = json.loads(contents)

print(f"I know your favorite number is {favorite_number}!")
