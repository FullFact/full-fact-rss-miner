import feedparser
from tinydb import Query
import time

def max_entry_date(feed):
    """Return the max published time in all entries of a feed"""
    entry_pub_dates = tuple(
        e.get('published_parsed') for e in feed.entries if 'published_parsed' in e
    )
    if entry_pub_dates:
        return max(entry_pub_dates)

    return None


def fetch_new_entries(source, db):
    """ Returns a list of new entries from a feed

    Looks up metadata and does not return entries already seen

    Parameters
    ----------
    source: dict
        keys name and url for the data source
    db: TinyDB
        Database for the metadata

    Returns
    -------
    list:
        Entries that have not yet been seen (may be empty)
    """

    name = source['name']
    url = source['url']

    # Check if we have seen this feed before
    src = Query()
    result = db.table('meta').get(src.name == name)

    if not result:
        # Add new meta data and return all entries
        new_feed = feedparser.parse(url)

        # check last updated field exists and populate with latest article if not
        updated, updated_parsed = get_last_updated_times(new_feed)

        data = {
            'name': name,
            'updated': updated,
            'updated_parsed': updated_parsed,
            'title': new_feed.feed.title,
            'subtitle': new_feed.feed.subtitle,
            'url': url,
            'max_entry_date': max_entry_date(new_feed),
            'etag': new_feed.get('etag'),
            'modified': new_feed.get('modified')
        }
        db.table('meta').insert(data)
        entries = new_feed.entries

    if result:
        # Try using get etag or last modified date to minimise bandwidth
        etag = result.get('etag', None)
        modified = result.get('modified', None)

        new_feed = feedparser.parse(url, etag=etag, modified=modified)

        entries = []
        if new_feed.entries:
            # Additonal filtering to check using the etag or last modified date worked.
            # This depends on whether the server is setup to make use of them so is
            # out of our control.
            prev_max_date = result['max_entry_date']

            # Filter entries to only keep those not seen before
            entries = [e for e in new_feed.entries
                         if e.get('published_parsed') > prev_max_date]  # noqa

            n_filtered = len(new_feed.entries) - len(entries)
            print('{} articles filtered out as already processed'.format(n_filtered))
            print('{} new articles'.format(len(entries)))

            if entries:
                # Update metadata

                # check last updated field exists and populate with latest article if not
                updated, updated_parsed = get_last_updated_times(new_feed)

                data = {
                    'name': name,
                    'updated': updated,
                    'updated_parsed': updated_parsed,
                    'title': new_feed.feed.title,
                    'subtitle': new_feed.feed.subtitle,
                    'url': url,
                    'max_entry_date': max_entry_date(new_feed),
                    'etag': new_feed.get('etag'),
                    'modified': new_feed.get('modified')
                }

                db.table('meta').update(data, eids=[result.eid])

    return entries


def get_last_updated_times(feed):

    if not feed.feed.get('updated'):
        updated_parsed = max_entry_date(feed)
        # Format as: 'Sun, 14 May 2017 14:35:21 GMT'
        updated = time.strftime('%a, %d %b %Y %H:%M:%S %Z')
    else:
        updated_parsed = feed.feed.updated_parsed
        updated = feed.feed.updated

    return updated, updated_parsed
