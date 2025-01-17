import requests

# Define the Emoji class
class Emoji:
    def __init__(self, name: str, group: str, category: str, html: str, unicode: str) -> None:
        self.name = name
        self.group = group
        self.category = category
        self.html = html
        self.unicode = unicode
    
    # display info
    def display_info(self) -> None:
        print(self.name)
        print(self.group)
        print(self.category)
        print(self.html)
        print(self.unicode)

    # when printed, the instance of the class will return its unicode
    def __str__(self) -> str:
        return chr(int(self.unicode.removeprefix("U+"), 16))

# Function to fetch data and return it
def fetch_emoji_data() -> dict[str: str | list[str]] | None:
    url: str = f"https://emojihub.yurace.pro/api/all"
    response: requests.Response = requests.get(url)

    if response.status_code == 200:
        emoji_data: dict[str: str | list[str]] = response.json()
        return emoji_data
    else:
        print(f"Error fetching data for emojis.")
        return None
    
# Create a Emoji object using the data
def create_emoji(emoji_json) -> Emoji:
    emoji: Emoji = Emoji(name=emoji_json["name"], 
                         group=emoji_json["group"], 
                         category=emoji_json["category"], 
                         html=emoji_json["htmlCode"][0], 
                         unicode=emoji_json["unicode"][0])

    return emoji


print()
print("Welcome to the Emoji Tracker!")
print("This app lets you see and track emojis!")
print()
# store all the emoji objects
emojis: list[str] = []

emoji_data: dict[str: str | list[str]] | None = fetch_emoji_data()

# Main program logic
while True:
    user_input: str = input("What emoji would you like the information of? Please type in its name below, or all if you would like to see your options: \n").lower().strip()
    print()
    print("Loading...")

    # filter through every emoji's information and find the emoji that's name matches the user's input 
    emoji: list | dict[str: str | list[str]] = list(filter(lambda list_item: 
                                                           True if user_input == list_item["name"] 
                                                           else True if user_input == "all"
                                                           else False, emoji_data))

    # error handling: if emoji isn't found, continue in loop
    if not emoji:
        print("That doesn't seem to be a valid emoji, please try again. \n")
        continue
    elif len(emoji) > 1:
        for each_emoji in emoji:
            print(each_emoji["name"])
        
        print()
        continue
    
    # converting the emoji value, which is a list, to a dictionary
    emoji = emoji[0]
    
    # create an emoji object
    emoji_obj: Emoji = create_emoji(emoji)
    
    # display emoji information
    print(emoji_obj)
    emoji_obj.display_info()

    # append the emoji to our list
    emojis.append(emoji_obj)

    print()
    keep_going = input("Track another emoji (y/n): ").lower().strip()
    if keep_going == "n":
        break

# display summary to user
print()
print("Here's the emojis you looked at today!:")
for emoji in emojis: print(f"{emoji.name}: {emoji}")