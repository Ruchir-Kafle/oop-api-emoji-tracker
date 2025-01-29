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
        character_label.configure(text=f"Character: {chr(int(self.unicode.removeprefix("U+"), 16))}")

        name_label.configure(text=f"Name: {self.name}")

        group_label.configure(text=f"Group: {self.group}")

        category_label.configure(text=f"Category: {self.category}")
        
        html_label.configure(text=f"HTML Code: {self.html}")

        html_label.configure(text=f"Unicode: {self.unicode}")

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
def create_emoji() -> Emoji:

    user_input: str = entry.get().lower()

    entry.delete(0, len(user_input))

    # filter through every emoji's information and find the emoji that's name matches the user's input 
    emoji_json: list | dict[str: str | list[str]] = list(filter(lambda list_item: 
                                                           True if user_input == list_item["name"] 
                                                           else True if user_input == "all"
                                                           else False, 
                                                           emoji_data))

    # error handling: if emoji isn't found, continue in loop
    if not emoji_json:
        print("That doesn't seem to be a valid emoji, please try again. \n")
    else:
        # converting the emoji value, which is a list, to a dictionary
        emoji_json = emoji_json[0]

    emoji: Emoji = Emoji(name=emoji_json["name"], 
                         group=emoji_json["group"], 
                         category=emoji_json["category"], 
                         html=emoji_json["htmlCode"][0], 
                         unicode=emoji_json["unicode"][0])

    # append the emoji to our list
    emojis.append(emoji)

    # display emoji information
    emoji.display_info()

# list of emojis the user tracks
emojis: list[str] = []

# all emoji data
emoji_data: dict[str: str | list[str]] | None = fetch_emoji_data()

# boolean deciding whether the main loop will run or not
run: bool = True

window: tk.Tk = tk.Tk()
window.geometry("350x350")
window.title("Emoji Tracker App")

# grid is created implictily based on largest length of constituent elements
# sticky allows elements to always be aligned to a part of the cell
welcome_label: tk.Label = tk.Label(window, text="Welcome to the Emoji Tracker!")
welcome_label.grid(row=0, column=0, columnspan=2, sticky="W")

description_label: tk.Label = tk.Label(window, text="This app lets you see and track emojis!")
description_label.grid(row=1, column=0, columnspan=2, sticky="W")

prompt_label: tk.Label = tk.Label(window, text="Enter an emoji's name:")
prompt_label.grid(row=2, column=0, columnspan=1, sticky="W", pady=10)

entry: tk.Entry = tk.Entry(window)
entry.grid(row=2, column=1, columnspan=1, sticky="W", pady=10)

button: tk.Button = tk.Button(window, text="Find", command=create_emoji)
button.grid(row=3, column=1, columnspan=1, sticky="W", pady=10)

character_label: tk.Label = tk.Label(window, text=f"Character: ")
character_label.grid(row=4, column=0, columnspan=1, sticky="W")

name_label: tk.Label = tk.Label(window, text=f"Name: ")
name_label.grid(row=5, column=0, columnspan=1, sticky="W")

group_label: tk.Label = tk.Label(window, text=f"Group: ")
group_label.grid(row=6, column=0, columnspan=1, sticky="W")

category_label: tk.Label = tk.Label(window, text=f"Category: ")
category_label.grid(row=7, column=0, columnspan=1, sticky="W")

html_label: tk.Label = tk.Label(window, text=f"HTML Code: ")
html_label.grid(row=8, column=0, columnspan=1, sticky="W")

html_label: tk.Label = tk.Label(window, text=f"Unicode: ")
html_label.grid(row=9, column=0, columnspan=1, sticky="W")

window.mainloop()