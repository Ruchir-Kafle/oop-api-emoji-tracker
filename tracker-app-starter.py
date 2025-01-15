import requests
import json
import random

# Define the Fruit class
class Fruit:
    def __init__(self, name, family, genus, calories, sugar):
        self.name = name
        self.family = family
        self.genus = genus
        self.calories = calories
        self.sugar = sugar

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Family: {self.family}")
        print(f"Calories: {self.calories}")
        print(f"Sugar: {self.sugar}")

# Function to fetch data and return it
def fetch_fruit_data(fruit_name):
    url = f"https://pokeapi.co/api/v2/pokemon/ditto"
    response = requests.get(url)

    if response.status_code == 200:
        fruit_data = response.json()
        return fruit_data
    else:
        print(f"Error fetching data for {fruit_name}.")
        return None
    
# Create a Fruit object using the data
def create_fruit(fruit_json):
    ... # :o

print()
print("Welcome to the Fruit Tracker!")
print("Track the nutritional values you've consumed in fruits today!")
print()
# store all the fruit objects
fruits = []
calories = 0
sugar = 0

# Main program logic
while True:
    user_input = input("Enter a fruit: ").lower().strip()
    print()
    print(random.choice(["Yummmm", "Tasty :P", "I'll take a bite of that!", "Great choice!"]))
    print("Loading...")

    # fetch fruit data using the API
    fruit_data = fetch_fruit_data(user_input)

    # error handling: if fruit isn't found, continue in loop
    if not fruit_data:
        continue
    
    # create an fruit object
    fruit_obj = create_fruit(fruit_data)
    fruit_obj.display_info()
    # append the fruit to our list
    fruits.append(fruit_obj)

    print()
    keep_going = input("Track another fruit (y/n): ").lower().strip()
    if keep_going == "n":
        break

# display summary to user
print()
print("Here's your fruity breakdown for today:")
for fruit in fruits:
    calories += fruit.calories
    sugar += fruit.sugar
print(f"Calories: {calories}")
print(f"Sugar: {sugar}")