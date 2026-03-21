from pathlib import Path
import json

# 10.11 ask for user's favorite number
favorite_number = input("What is your favorite number? ")

path = Path('favorite_number.json')
contents = json.dumps(favorite_number)
path.write_text(contents)
