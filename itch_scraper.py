import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List

# fetches HTML, returns BeautifulSoup object
def fetch_soup(url: BeautifulSoup) -> BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

# converts text to a tokenizable format
def clean_text(text) -> str:
    # remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # # remove colons from section headers
    text = re.sub(r'(?m)^\s*(\w+):', r'\1', text)
    # remove all punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # normalize multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text)
    # trim leading/trailing spaces
    text = text.strip()
    # lowercase
    text = text.lower()
    return text

def pretty_print_json(data: str) -> None:
  pretty_json = json.dumps(data, indent=4)
  print(pretty_json)

def get_application_json(soup: BeautifulSoup) -> str:
  application_data = soup.find_all('script', type='application/ld+json')
  game_data = application_data[1]
  json_data = json.loads(game_data.get_text())
  return json_data

def get_tags(soup: BeautifulSoup) -> List[str]:
  tag = soup.find('script', type='application/ld+json')
  json_data = json.loads(tag.get_text())
  tag_data_list = json_data["itemListElement"]
  tag_list = map(lambda x: x["item"]["name"], tag_data_list)
  return list(tag_list)

def get_title(soup: BeautifulSoup) -> str:
  json_data = get_application_json(soup)
  if not json_data["name"]:
     return None
  return json_data["name"]

def get_aggregate_rating(soup: BeautifulSoup) -> float:
  json_data = get_application_json(soup)
  if not json_data["aggregateRating"]:
     return None
  return float(json_data["aggregateRating"]["ratingValue"])

def get_rating_count(soup: BeautifulSoup) -> int:
  json_data = get_application_json(soup)
  if not json_data["aggregateRating"]:
     return None
  return int(json_data["aggregateRating"]["ratingCount"])

def get_logline(soup: BeautifulSoup) -> str:
  json_data = get_application_json(soup)
  if not json_data["description"]:
     return None
  return json_data["description"]
    
def get_description(soup: BeautifulSoup) -> str:
    description_html = soup.find(class_="formatted_description user_formatted")
    if not description_html:
        return None
    text = description_html.get_text(" ")
    # text = clean_text(text)
    return text
    
# warning! this takes a long time
# count -> how many comments to scrape
# recent -> scrapes the most recent `count`` comments

def get_comments(soup: BeautifulSoup, url: str,  page_count: int = 2, recent: bool = True) -> List[str]:
    """
    Gets the comments for the itch.io game specified in the URL.

    Parameters:
    url (str): URL for an itch.io game
    pages (int): Pages of comments to scrape (40 comments per page).
    recent (bool): If true, this will scrape the most recent `count` games. If false, 
    this will scrape the oldest `count` games.

    Returns:
    comments (List[str]): A list of comments.
    """

    comment_label = soup.find(class_="page_label")
    comment_label_text = comment_label.get_text(" ")
    comment_count = re.findall(r"\d{1,3}(?:,\d{3})*", comment_label_text)[2]
    comment_count = int(comment_count.replace(',', ''))

    base_url = f"{url}/comments?after="

    comments = []

    for page in range(1, page_count + 1):
      if not recent:
        new_url = base_url + str((page-1) * 40)
      else:
        new_url = base_url + str(comment_count - page * 40)

      print(f"\npage {page} - {new_url}\n")

      comment_soup = fetch_soup(new_url)
      page_comments = comment_soup.find_all(class_="post_body user_formatted")
      comments += page_comments
      
    comments = list(map(lambda x: x.get_text(), comments))
    return comments