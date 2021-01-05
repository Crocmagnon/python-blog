import itertools

from django.conf import settings


class DummyArticleWithCode:
    has_code = True


class DummyArticleNoCode:
    has_code = False


class DummyNonAuthenticatedUser:
    is_authenticated = False


class DummyAuthenticatedUser:
    is_authenticated = True


def offline_context():
    article_possibilities = [None, DummyArticleWithCode(), DummyArticleNoCode()]
    user_possibilities = [DummyAuthenticatedUser(), DummyNonAuthenticatedUser()]
    goatcounter_possibilities = [None, settings.GOATCOUNTER_DOMAIN]
    all_possibilities = [
        article_possibilities,
        user_possibilities,
        goatcounter_possibilities,
    ]
    for _tuple in itertools.product(*all_possibilities):
        yield {
            "STATIC_URL": settings.STATIC_URL,
            "article": _tuple[0],
            "user": _tuple[1],
            "goatcounter_domain": _tuple[2],
        }
