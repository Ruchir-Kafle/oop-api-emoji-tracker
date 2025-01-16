import requests
import json
import random

# Define the Emoji class
class Emoji:
    def __init__(self, *args):
        print(args)
        self.name = args[0]
        self.group = args[1]
        self.category = args[2]
        self.html = args[3][0]
        self.unicode = args[4][0]

    def display_info(self):
        print(self.name)
        print(self.group)
        print(self.category)
        print(self.html)
        print(self.unicode)

    def __str__(self):
        return chr(int(self.unicode.removeprefix("U+"), 16))

# Function to fetch data and return it
def fetch_emoji_data():
    url = f"https://emojihub.yurace.pro/api/all"
    response = requests.get(url)

    if response.status_code == 200:
        emoji_data = response.json()
        return emoji_data
    else:
        print(f"Error fetching data for emojis.")
        return None
    
# Create a Emoji object using the data
def create_emoji(emoji_json):
    emoji = Emoji(*emoji_json.values())

    return emoji


print()
print("Welcome to the Emoji Tracker!")
print("Emojis, yipee!")
print()
# store all the fruit objects
emojis = []
calories = 0
sugar = 0

emoji_data = fetch_emoji_data()

# Main program logic
while True:
    user_input = input("What emoji would you like the information of? Please type in its name below: \n").lower().strip()
    print()
    print("Loading...")

    emoji = list(filter(lambda list_item: list_item if user_input == list_item["name"] else None, emoji_data))[0]

    # error handling: if fruit isn't found, continue in loop
    if not emoji:
        continue
    
    # create an fruit object
    emoji_obj = create_emoji(emoji)
    emoji_obj.display_info()
    # append the fruit to our list
    emojis.append(emoji_obj)

    print()
    keep_going = input("Track another fruit (y/n): ").lower().strip()
    if keep_going == "n":
        break

# display summary to user
print()
print("Here's your fruity breakdown for today:")
for fruit in emoji:
    calories += fruit.calories
    sugar += fruit.sugar
print(f"Calories: {calories}")
print(f"Sugar: {sugar}")