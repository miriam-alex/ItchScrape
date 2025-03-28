import itch_scraper as itch
import json
from tqdm import tqdm

# sample usage

# url = "https://frannym.itch.io/10questions"

# json = itch.get_data(url)
# itch.pretty_print_json(json)

# to scrape from the urls.txt
print('Enter the path to your urls.txt file')
txt_path = input()

print('Enter the name of your output.json file')
output_path = input()

with open(txt_path, 'r') as file:
  content = file.read()

game_jsons = []

lines = content.splitlines() # Splits into lines
for line in tqdm(lines):
  url = line.strip() 
  json_obj = itch.get_data(url)
  if json_obj:
    game_jsons.append(json_obj)

results = json.dumps(game_jsons, indent=4)
 
# Writing to sample.json
with open(output_path, "w") as outfile:
    outfile.write(results)

