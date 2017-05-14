
from bs4 import BeautifulSoup
import requests


def fetch_article_content(entry, content_tag=None, header=None):
    """Return a list of all paragraph tags in the entry """

    response = requests.get(entry.link, headers=header)

    if not response.ok:
        raise IOError("Could not fetch article content, encountered: {} from {}".format(
            response.status_code, response.url))

    soup = BeautifulSoup(response.content, "html.parser")

    if content_tag:
        # Look up exact parent tag for all content
        parent_tag = soup.select(content_tag)
        if parent_tag:
            p_tags = parent_tag[0].find_all(name='p')
        else:
            p_tags = []
    else:
        # Guess by using the parent of the title tag
        p_tags = find_content_p_tags(soup)

    paragraphs = []

    for p in p_tags:

        # Get text and strip white space
        text = p.get_text()
        if text is not None:
            text = text.strip()
            paragraphs.append(text)

    return paragraphs


def find_content_p_tags(soup):

    # Detect title tag
    title_string = soup.find_all(string="Gordon Brown accuses Tories of 'waging war against poor'")[0]

    # Find the enclosing tag 
    enclosing_tag = title_string.find_parent().find_parent()

    # Find all p tags
    p_tags = enclosing_tag.find_all(name='p')

    # Filter out those that only contain 3 or less words
    p_tags = [p for p in p_tags if len(p.text.split()) > 3]

    return p_tags