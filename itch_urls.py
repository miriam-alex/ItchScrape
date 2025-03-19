from bs4 import BeautifulSoup

if __name__ == "__main__":
    with open("data/new_and_popular.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    game_thumbs = soup.find_all(class_="game_thumb")

    urls = []
    for element in game_thumbs:
        urls.append(element.a.get("href"))

    print("# of urls: ", len(urls))

    with open("new_and_popular_urls.txt", "w") as file:
        for item in urls:
            file.write(f"{item}\n")
