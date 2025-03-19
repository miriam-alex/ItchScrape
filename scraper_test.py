import itch_scraper as itch

url = "https://twoandahalfstudios.itch.io/a-date-with-death"

data = {}
soup = itch.fetch_soup(url)

data["title"] = itch.get_title(soup)
data["url"] = url
data["logline"] = itch.get_logline(soup)
rating = {}
rating["aggregate rating"] = itch.get_aggregate_rating(soup)
rating["rating count"] = itch.get_rating_count(soup)
data["rating"] = rating
data["tags"] = itch.get_tags(soup)
data["description"] = itch.get_description(soup)
data["comments"] = itch.get_comments(soup, url) 

itch.pretty_print_json(data)