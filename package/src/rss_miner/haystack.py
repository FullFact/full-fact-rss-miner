
from xml.etree.ElementTree import Element, SubElement
import time


def new_haystack(id, batch):
    """Return New root Haystack XML node"""

    haystack_attributes = {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "version": "2.0",
        "xsi:noNamespaceSchemaLocation": "http://fullfact.org/static/schema/haystack.xsd",
        "batch": batch,
        "id": id
    }

    return Element('haystack', haystack_attributes)


def write_to_haystack(haystack, source, entity, sentences):

    author_name = entity.get('author', default='Unknown')

    meta_attributes = {
        "authorname": author_name,
        "author": source['name'],
        "publication": "Online Article",
        "pdate": time.strftime('%Y-%m-%dT%H:%M:%SZ', entity.published_parsed),
        "url": entity.link
    }

    meta = SubElement(haystack, 'meta', meta_attributes)

    sentence_elements = []
    for sentence in sentences:
        tag = Element('s')
        tag.text = sentence
        sentence_elements.append(tag)

    meta.extend(sentence_elements)
