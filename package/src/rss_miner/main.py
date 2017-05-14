"""An RSS feed mining tool developed for Full Fact https://fullfact.org/"""

import argparse
import pathlib
import sys
import time
from xml.etree.ElementTree import ElementTree

import yaml
from tinydb import TinyDB

from . import PKG_DIR
from .content import fetch_article_content
from .feeds import fetch_new_entries
from .haystack import new_haystack, write_to_haystack
from .nlp import paragraphs_to_sentences
from .storage import insert_entry, serialization


def read_config(filename):

    content = yaml.load(stream=open(filename))

    feeds = content['feeds']
    config = content['config']

    # Use path objects
    config['output-folder'] = pathlib.Path(config['output-folder'])

    # fix user-agent header if lowercase
    if 'user-agent' in config['request-headers']:
        config['request-headers']['User-Agent'] = config['request-headers']['user-agent']
        del config['request-headers']['user-agent']

    # convert feeds into list of dictionaries
    data_sources = []
    for k in feeds.keys():
        s = feeds[k]
        s.update({'name': k})
        data_sources.append(s)

    return data_sources, config


def main(args):

    if not args.config_filepath:
        if not args.generate_config:
            raise ValueError('Expected arguments undefined.')
        else:
            reference_config_path = PKG_DIR / 'example_config.yml'
            content = reference_config_path.read_text()
            with open('example_config.yml', 'w') as output_config:
                output_config.write(content)
        sys.exit()

    # Read YAML file for config and feeds
    data_sources, config = read_config(args.config_filepath)

    # Initialise Data Storage
    name = config['meta-db-name'] + '.json'
    db = TinyDB(name, storage=serialization)

    now = time.strftime('%Y-%m-%d-%H:%M', time.localtime())
    haystack = new_haystack(batch=now, id='RSS-Feeds')

    for source in data_sources:
        print(source['name'] + ' - ',  end='')
        sys.stdout.flush()

        # Try to get more entries
        entries = fetch_new_entries(source=source, db=db)

        if entries:

            print('Fetching content ',  end='')
            sys.stdout.flush()

            for ent in entries:

                # Fetch Content
                paragraphs = fetch_article_content(ent, content_tag=source['content-tag'],
                                                   header=config['request-headers'])

                # Split into individual sentences
                sentences = paragraphs_to_sentences(paragraphs)

                write_to_haystack(haystack, source=source, entity=ent, sentences=sentences)

                # Store metadata in data base
                insert_entry(ent, db)

                time.sleep(0.5)
                print('.', end='')
                sys.stdout.flush()
        print('')
        sys.stdout.flush()

    # Write output
    tree = ElementTree(haystack)
    output_filename = 'feeds{date}.xml'.format(date=now)
    output_dir = config['output-folder']
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / output_filename
    tree.write(filepath.as_posix())
    print('Wrote haystack to {}'.format(filepath.as_posix()))


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-c', '--config', dest='config_filepath',
        help='Filename for the configuration yaml file to use.'
    )
    parser.add_argument(
        '-g', '--generate-config', action='store_true', dest='generate_config',
        help='Generate an example config file in the current directory for further editing'
    )

    return parser


def cli_entry_point():
    """This is the function that gets executed first from command line"""

    # Parse Arguments
    args = get_parser().parse_args()
    # Run program
    main(args)


if __name__ == '__main__':
    # If executed directly, this script will kick off the same entry point
    # as if the command line utility was invoked
    cli_entry_point()
