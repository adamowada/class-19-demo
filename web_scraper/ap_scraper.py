from bs4 import BeautifulSoup
import requests


def scraper(topic):
    # Scrape the top link
    response = requests.get(f"https://apnews.com/search?q={topic}#nt=navsearch")
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find("div", class_="SearchResultsModule-results")
    top_stories = search_results.find_all("div", class_="PagePromo-title")

    for story in top_stories:
        url = story.find("a")["href"]
        if url.startswith("https://apnews.com/article/"):
            break

    # Scrape the news story
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    story_body = soup.find("div", class_="RichTextStoryBody")
    story_p_elements = story_body.find_all("p")

    # Build string
    story = ""

    for elem in story_p_elements:
        story += elem.get_text()

    return url, story


if __name__ == "__main__":
    print(scraper("cars"))
