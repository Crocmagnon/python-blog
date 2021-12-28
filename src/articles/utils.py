import re

import markdown
from bs4 import BeautifulSoup
from django.conf import settings
from markdown.extensions.codehilite import CodeHiliteExtension

from articles.markdown import LazyLoadingImageExtension


def build_full_absolute_url(request, url):
    if request:
        return request.build_absolute_uri(url)
    else:
        return (settings.BLOG["base_url"] + url)[::-1].replace("//", "/", 1)[::-1]


def format_article_content(content):
    md = markdown.Markdown(
        extensions=[
            "extra",
            "admonition",
            CodeHiliteExtension(linenums=False, guess_lang=False),
            LazyLoadingImageExtension(),
        ]
    )
    content = re.sub(r"(\s)#(\w+)", r"\1\#\2", content)
    return md.convert(content)


def truncate_words_after_char_count(text, char_count):
    total_length = 0
    text_result = []
    for word in text.split():
        if len(word) + 1 + total_length > char_count:
            break
        text_result.append(word)
        total_length += len(word) + 1
    return " ".join(text_result) + "..."


def find_first_paragraph_with_text(html):
    bs = BeautifulSoup(html, "html.parser")
    paragraph = bs.find("p", recursive=False)
    text = paragraph.text.strip()
    while not text:
        try:
            paragraph = paragraph.next_sibling
            text = paragraph.text.strip()
        except Exception:
            break
    return text
