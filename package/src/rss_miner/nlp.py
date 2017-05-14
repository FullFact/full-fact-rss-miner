
import collections
import re


def paragraphs_to_sentences(paragraph_list):
    """Convert a list of paragraphs into a list of sentences"""

    nested_list = [text_to_sentences(p) for p in paragraph_list]

    sentence_list = flatten_nested_list(nested_list)

    return list(sentence_list)


def text_to_sentences(text):
    """ Split input text into a list of sentences. """

    # Split on . or ? or ! followed by white space.
    # A detailed demo is availiable at https://regex101.com/r/dNFhgE/4
    regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s"

    result = re.split(pattern=regex, string=text, flags=re.MULTILINE)

    # Strip white space fro each sentence
    sentences = [s.strip() for s in result]

    # Drop any empty sentences
    sentences = [s for s in sentences if s]

    return sentences


def flatten_nested_list(nested_list):
    """Flattern a list by returning all the elements as a generator"""

    for el in nested_list:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten_nested_list(el)
        else:
            yield el