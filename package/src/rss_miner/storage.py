
from tinydb_serialization import SerializationMiddleware

from time import struct_time
import time

from tinydb_serialization import Serializer


class DateTimeSerializer(Serializer):
    OBJ_CLASS = struct_time  # The class this serializer handles

    def encode(self, obj):
        return time.strftime('%Y-%m-%dT%H:%M:%S %Z', obj)

    def decode(self, s):
        return time.strptime(s, '%Y-%m-%dT%H:%M:%S %Z')


serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')


def insert_entry(entry, db):
    """Extract and store required information in db"""

    data = {
        'feed_id': 'foo',
        'title': entry.title,
        'id': entry.id,
        'link': entry.link,
        'published': entry.published,
        'published_parsed': entry.published_parsed,
        'authors': entry.get('authors'),
        'tags': entry.get('tags')
    }

    db.table('entries').insert(data)
