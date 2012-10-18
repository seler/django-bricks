import random
import re
import unicodedata
import unidecode
import itertools

from django.utils.encoding import smart_unicode
from django.template import defaultfilters


SLUG_OK = '-_~'


def mozilla_slugify(s, ok=SLUG_OK, lower=True, spaces=False):
    """
    Mozilla-team implementation of slugify.
    Borrowed from https://github.com/mozilla/unicode-slugify
    """
    rv = []
    for c in unicodedata.normalize('NFKC', smart_unicode(s)):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in ok:
            rv.append(c)
        if cat == 'Z':  # space
            rv.append(' ')
    new = ''.join(rv).strip()
    if not spaces:
        new = re.sub('[-\s]+', '-', new)
    return new.lower() if lower else new


def smart_slugify(s):
    return defaultfilters.slugify(unidecode.unidecode(s))


def firstof(iterable, test=bool, default=None, index=False):
    if index:
        return next(((i, x) for i, x in enumerate(iterable) if test(x)), default)
    return next((x for x in iterable if test(x)), default)


def make_random_string(length=8, universe='', small_letters=True,
                       big_letters=True, numbers=True, special=True,
                       force_all_types=True, avoid_ambiguous=False):

    pu = (
        'abcdefghijklmnoqprstuwvxyz',
        'ABCDEFGHIJKLMNOPQRSTUWVXYZ',
        '0123456789',
        '!@#%$&*^',
    )

    ambiguous_characters = 'O01lIqg'

    custom_universe = True
    if not universe:
        universe = ''
        if small_letters:
            universe += pu[0]
        if big_letters:
            universe += pu[1]
        if numbers:
            universe += pu[2]
        if special:
            universe += pu[3]
        custom_universe = False

    def mkstring(length, universe):
        string = ''
        for i in range(length):
            string += random.choice(universe)
        return string

    string_ok = False

    if avoid_ambiguous:
        for c in ambiguous_characters:
            universe = universe.replace(c, '')

    while not string_ok:
        string = mkstring(length, universe)
        string_ok = all((
            any(map(lambda i: i in string, pu[0])) or not small_letters,
            any(map(lambda i: i in string, pu[1])) or not big_letters,
            any(map(lambda i: i in string, pu[2])) or not numbers,
            any(map(lambda i: i in string, pu[3])) or not special,
        )) or not force_all_types or custom_universe

    return string


def groups(iterable, n):
    """
    Groups *iterable* by *n* elements each.
    """
    for i in range(len(iterable)):
        if i % n:
            yield iterable[i - 1:i + n - 1]


def chounks(iterable, n):
    """
    Divides list *l* to *n* chunks.
    """
    return (iterable[i:i + n] for i in range(0, len(iterable), n))


def grouper(iterable, n, fillvalue=None):
    return itertools.izip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)
