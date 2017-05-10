
# from validator import validate
from tinydb import TinyDB, Query
from storage import serialization, insert_entry
from source_feeds import fetch_new_entries
from source_articles import fetch_article_content, paragraphs_to_sentences
import time
import sys


def read_config():

    # sources are dictionaries with 
    data_sources = [
        {
            'name': 'bbc', 
            'url': "http://feeds.bbci.co.uk/news/politics/rss.xml",
            'article_tag': 'div.story-body__inner'
        }, 
        {
            'name': 'ft', 
            'url': "http://feeds2.feedburner.com/ft/westminster",
            'article_tag': 'div.entry-content'
        }, 
        {
            'name': 'gaurdian', 
            'url': "https://www.theguardian.com/politics/rss",
            'article_tag': 'div.content__main'
        } 
    ]

    return data_sources


def main(args):

    # Read YAML file for config and feeds
    data_sources = read_config()

    # Initialise Data Storage 
    db = TinyDB('db.json', storage=serialization)

    for source in data_sources:
        # Try to get more entries 
        entries = fetch_new_entries(source=source, db=db)

        if entries:
            for ent in entries:
                # Store metadata in data base
                insert_entry(ent, db)

                # Fetch Content
                paragraphs = fetch_article_content(ent, source['article_tag'])

                # Split into individual sentences
                sentences = paragraphs_to_sentences(paragraphs)

                filename = 'articles/' + ent.title + '.txt'
                with open(filename, 'w') as f:
                    data = '\n-----\n'.join(sentences)
                    f.write(data)

                time.sleep(0.1)
                print('.', end='')
                sys.stdout.flush()

                # Write to Haystack format




# if validate("path/to/file.xml", "path/to/scheme.xsd"):
#     print('Valid! :)')
# else:
#     print('Not valid! :(')