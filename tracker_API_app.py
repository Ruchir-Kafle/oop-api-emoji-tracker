import requests
import tkinter as tk

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
        print(f"Name: {self.name}")
        print(f"Group: {self.group}")
        print(f"Category: {self.category}")
        print(f"HTML Code: {self.html}")
        print(f"Unicode: {self.unicode}")

    # when printed, the instance of the class will return its unicode
    def __str__(self) -> str:
        return chr(int(self.unicode.removeprefix("U+"), 16))

# Function to fetch emoji data and return it
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

# list of emojis the user tracks
emojis: list[str] = []

# all emoji data
emoji_data: dict[str: str | list[str]] | None = fetch_emoji_data()

# boolean deciding whether the main loop will run or not
run: bool = True

window: tk.Tk = tk.Tk()
window.geometry("350x350")
window.title("Emoji Tracker App")

welcome_label: tk.Label = tk.Label(window, text="Welcome to the Emoji Tracker!", anchor="w").grid(row=0, column=2, columnspan=3)
description_label: tk.Label = tk.Label(window, text="This app lets you see and track emojis!", anchor="w").grid(row=1, column=2, columnspan=3)

# Main program logic
while run:
    user_input: str = input("What emoji would you like the information of? Please type in its name below, or all if you would like to see your options: \n").lower().strip()
    print("\nLoading...")

    # filter through every emoji's information and find the emoji that's name matches the user's input 
    user_emoji: list | dict[str: str | list[str]] = list(filter(lambda list_item: 
                                                           True if user_input == list_item["name"] 
                                                           else True if user_input == "all"
                                                           else False, emoji_data))

    # error handling: if emoji isn't found, continue in loop
    if not user_emoji:
        print("That doesn't seem to be a valid emoji, please try again. \n")
        continue
    elif len(user_emoji) > 1:
        for each_emoji in user_emoji:
            print(each_emoji["name"])
        
        print()
        continue
    
    # converting the emoji value, which is a list, to a dictionary
    user_emoji = user_emoji[0]
    
    # create an emoji object
    emoji_obj: Emoji = create_emoji(user_emoji)
    
    # append the emoji to our list
    emojis.append(emoji_obj)

    # display emoji information
    print(emoji_obj)
    emoji_obj.display_info()

    # while loop to keep asking the user if they would like to track another emoji if they keep entering invalid inputs
    while True:
        keep_going: str = input("\nTrack another emoji (y/n): \n").lower().strip()

        if keep_going == "y":
            break
        elif keep_going == "n":
            run = False
            break
        else:
            print("\nThat doesn't seem to be a valid option, please try again.")

# display summary to user
print("\nHere's the emojis you looked at today!:")
for emoji in emojis: print(f"{emoji.name}: {emoji}")