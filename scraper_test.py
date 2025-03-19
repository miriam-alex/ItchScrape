import itch_scraper as itch
import json

# sample usage

# url = "https://twoandahalfstudios.itch.io/a-date-with-death"

# json = itch.get_data(url)
# itch.pretty_print_json(json)

# to scrape from the urls.txt
print('Enter the path to your urls.txt file')
txt_path = input()

with open(txt_path, 'r') as file:
  content = file.read()

game_jsons = []

lines = content.splitlines() # Splits into lines
for line in lines:
  url = line.strip() 
  json_obj = itch.get_data(url)
  game_jsons.append(json_obj)

results = json.dumps(game_jsons, indent=4)
 
# Writing to sample.json
with open("top_rated_games.json", "w") as outfile:
    outfile.write(results)

