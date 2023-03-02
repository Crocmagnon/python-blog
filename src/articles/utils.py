import re

import markdown
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

from articles.markdown import LazyLoadingImageExtension


def build_full_absolute_url(request: WSGIRequest | None, url: str) -> str:
    if request:
        return request.build_absolute_uri(url)
    return (settings.BLOG["base_url"] + url)[::-1].replace("//", "/", 1)[::-1]


def format_article_content(content: str) -> str:
    md = markdown.Markdown(
        extensions=[
            "extra",
            "admonition",
            TocExtension(anchorlink=True),
            CodeHiliteExtension(linenums=False, guess_lang=False),
            LazyLoadingImageExtension(),
        ],
    )
    content = re.sub(r"(\s)#(\w+)", r"\1\#\2", content)
    return md.convert(content)


def truncate_words_after_char_count(text: str, char_count: int) -> str:
    total_length = 0
    text_result = []
    for word in text.split():
        if len(word) + 1 + total_length > char_count:
            break
        text_result.append(word)
        total_length += len(word) + 1
    return " ".join(text_result) + "..."


def find_first_paragraph_with_text(html: str) -> str:
    bs = BeautifulSoup(html, "html.parser")
    paragraphs = bs.find_all("p", recursive=False)
    for paragraph in paragraphs:
        if paragraph.text.strip():
            return paragraph.text
    return ""
