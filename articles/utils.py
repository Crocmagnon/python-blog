from django.conf import settings


def build_full_absolute_url(request, url):
    if request:
        return request.build_absolute_uri(url)
    else:
        return (settings.BLOG["base_url"] + url)[::-1].replace("//", "/", 1)[::-1]
