from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import (
    IMAGE_LINK_RE,
    IMAGE_REFERENCE_RE,
    ImageInlineProcessor,
    ImageReferenceInlineProcessor,
)


class LazyImageInlineProcessor(ImageInlineProcessor):
    def handleMatch(self, m, data):  # type: ignore[no-untyped-def] # noqa: N802
        el, match_start, index = super().handleMatch(m, data)
        if el is not None:
            el.set("loading", "lazy")
        return el, match_start, index  # type: ignore[no-untyped-def]


class LazyImageReferenceInlineProcessor(ImageReferenceInlineProcessor):
    def makeTag(self, href, title, text):  # type: ignore[no-untyped-def] # noqa: N802
        el = super().makeTag(href, title, text)
        if el is not None:
            el.set("loading", "lazy")
        return el


class LazyLoadingImageExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802
        md.inlinePatterns.register(
            LazyImageInlineProcessor(IMAGE_LINK_RE, md),
            "image_link",
            150,
        )
        md.inlinePatterns.register(
            LazyImageReferenceInlineProcessor(IMAGE_REFERENCE_RE, md),
            "image_reference",
            140,
        )
        md.registerExtension(self)
