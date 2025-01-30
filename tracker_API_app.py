import requests
import tkinter as tk
from tkinter import ttk

# Define the Emoji class
class Emoji:
    def __init__(self, name: str, group: str, category: str, html: str, unicode: str) -> None:
        self.name = name
        self.group = group
        self.category = category
        self.html = html
        self.unicode = unicode

        self.character = chr(int(self.unicode.removeprefix("U+"), 16))
    
    # display info
    def display_info(self) -> None:
        character_label.configure(text=f"Character: {self.character}")
        name_label.configure(text=f"{self.name}")
        group_label.configure(text=f"Group: {self.group}")
        category_label.configure(text=f"Category: {self.category}")
        html_label.configure(text=f"HTML Code: {self.html}")
        unicode_label.configure(text=f"Unicode: {self.unicode}")
        error_message.configure(text=f"")

        emoji_string: str = ""

        for emoji in [emoji + ",\n" for emoji in emojis]:
            emoji_string += emoji

        emojis_label.configure(text=f"{emoji_string}")

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
def create_emoji(*args) -> Emoji:

    user_input: str = user_entry.get().lower()

    user_entry.delete(0, len(user_input))

    # filter through every emoji's information and find the emoji that's name matches the user's input 
    emoji_json: list | dict[str: str | list[str]] = list(filter(lambda list_item: 
                                                           True if user_input == list_item["name"] 
                                                           else False, 
                                                           emoji_data))

    # error handling: if emoji isn't found, continue in loop
    if not emoji_json:

        error_message.configure(text=f"That doesn't seem to be a valid emoji, please try again.")
    
    else:
    
        # converting the emoji value, which is a list, to a dictionary
        emoji_json = emoji_json[0]

        # creating the emoji object
        emoji: Emoji = Emoji(name=emoji_json["name"], 
                            group=emoji_json["group"], 
                            category=emoji_json["category"], 
                            html=emoji_json["htmlCode"][0], 
                            unicode=emoji_json["unicode"][0])

        # append the emoji to our list
        emojis.append(f"{emoji.name} {emoji.character}")

        # display emoji information
        emoji.display_info()

# list of emojis the user tracks
emojis: list[str] = []

# all emoji data
emoji_data: dict[str: str | list[str]] | None = fetch_emoji_data()

# boolean deciding whether the main loop will run or not
run: bool = True

# create window
window: tk.Tk = tk.Tk()
window.geometry("500x600")
window.title("Emoji Tracker App")

# styling
style: ttk.Style = ttk.Style()
style.theme_use("winnative")
style.configure("TLabel", font=("Gabriola", 13))
style.configure("TButton", font=("Impact", 16))
style.configure("TEntry", font=("Impact", 16), padding=5)

# welcome label
# grid is created implictily based on largest length of constituent elements
# sticky allows elements to always be aligned to a part of the cell
welcome_label: ttk.Label = ttk.Label(window, text="Welcome to the Emoji Tracker!", style="TLabel")
welcome_label.grid(row=0, column=0, columnspan=2)

# description label
description_label: ttk.Label = ttk.Label(window, text="This app lets you see and track emojis!", style="TLabel")
description_label.grid(row=1, column=0, columnspan=2)

# prompt label
prompt_label: ttk.Label = ttk.Label(window, text="Enter an emoji's name:", style="TLabel")
prompt_label.grid(row=2, column=0, columnspan=1, sticky="W", pady=10)

# entry box
user_entry: ttk.Entry = ttk.Entry(window, style="TEntry")
user_entry.grid(row=2, column=1, columnspan=1, sticky="WE")

# submit button
find_button: ttk.Button = ttk.Button(window, text="Find", command=create_emoji, style="TButton")
find_button.grid(row=3, column=1, columnspan=1, sticky="WE")
# when focused and enter is pressed, create emoji is called
find_button.bind("<Return>", create_emoji)

# character label
character_label: ttk.Label = ttk.Label(window, text=f"Character: ", style="TLabel")
character_label.grid(row=4, column=0, columnspan=1, sticky="W")

# name label
# before name
precursor_name_label: ttk.Label = ttk.Label(window, text=f"Name: ", style="TLabel")
precursor_name_label.grid(row=5, column=0, columnspan=1, sticky="W")
# actual name label
name_label: ttk.Label = ttk.Label(window, text=f"", wraplength=150, style="TLabel")
name_label.grid(row=5, column=1, columnspan=1, sticky="W")

# group label
group_label: ttk.Label = ttk.Label(window, text=f"Group: ", style="TLabel")
group_label.grid(row=6, column=0, columnspan=1, sticky="W")

# category label
category_label: ttk.Label = ttk.Label(window, text=f"Category: ", style="TLabel")
category_label.grid(row=7, column=0, columnspan=1, sticky="W")

# html label
html_label: ttk.Label = ttk.Label(window, text=f"HTML Code: ", style="TLabel")
html_label.grid(row=8, column=0, columnspan=1, sticky="W")

# unicode label
unicode_label: ttk.Label = ttk.Label(window, text=f"Unicode: ", style="TLabel")
unicode_label.grid(row=9, column=0, columnspan=1, sticky="W")

# tracked emojis label
# before emojis
precursor_emojis_label: ttk.Label = ttk.Label(window, text=f"Tracked Emojis: ", style="TLabel")
precursor_emojis_label.grid(row=10, column=0, columnspan=1, sticky="NSW")
# actual emojis label
emojis_label: ttk.Label = ttk.Label(window, text=f"{[emoji + "\n" for emoji in emojis]}", wraplength=150, style="TLabel")
emojis_label.grid(row=10, column=1, columnspan=1, sticky="W")

# error message label
error_message: ttk.Label = ttk.Label(window, text=f"", wraplength=150, style="TLabel")
error_message.grid(row=11, column=1, columnspan=1, pady=10)

# triggering the main loop
window.mainloop()