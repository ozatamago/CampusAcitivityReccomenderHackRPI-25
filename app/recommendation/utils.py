# app/recommendation/utils.py などに置く想定

from typing import Set

from .vocab import TAG_VOCAB

ALLOWED_TAGS = set(TAG_VOCAB)


def parse_tags(tag_string: str) -> Set[str]:
    """
    Parse a comma-separated tag string into a normalized set of tags.

    - Splits by comma
    - Strips whitespace
    - Lowercases tokens
    - Keeps only tags that are in TAG_VOCAB
    """
    if not tag_string:
        return set()

    raw_tokens = tag_string.split(",")
    tags = set()

    for token in raw_tokens:
        t = token.strip().lower()
        if not t:
            continue
        if t in ALLOWED_TAGS:
            tags.add(t)
        else:
            # For now: ignore unknown tags silently.
            # In the future, you could log a warning here.
            # current_app.logger.warning(f"Unknown tag '{t}' in tag_string='{tag_string}'")
            pass

    return tags

import re
from typing import Set


WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def parse_tokens(text: str) -> Set[str]:
    """
    Parse a free-form text into a normalized set of tokens.

    - Lowercases the text
    - Extracts alphanumeric “words” using a simple regex
    - Returns a set of unique tokens
    """
    if not text:
        return set()

    normalized = text.lower()
    tokens = set(WORD_RE.findall(normalized))
    return tokens
