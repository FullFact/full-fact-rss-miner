
from bs4 import BeautifulSoup
import requests
from utils import flatten_nested_list


def fetch_article_content(entry, article_tag):
    """Return a list of all paragraph tags in the entry """

    response = requests.get(entry.link)

    if not response.ok:
        raise IOError("Could not fetch article content, encountered: {}".format(response.status))

    soup = BeautifulSoup(response.content, "html.parser")

    article = soup.select(article_tag)[0]

    ps = article.find_all(name='p')

    # Get text and strip white space
    paragraphs = [p.get_text() for p in ps]
    paragraphs = [p.strip() for p in paragraphs if p is not None]

    return paragraphs


def paragraphs_to_sentences(paragraphs):
    """Return list of individual sentences from paragraphs"""

    import spacy
    nlp = spacy.load('en')

    docs = [nlp(p) for p in paragraphs]

    sents = [d.sents for d in docs]

    all_sents = flatten_nested_list(sents)

    return all_sents
