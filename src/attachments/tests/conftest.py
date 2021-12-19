import pytest


def replace_post_body(request):
    request.body = None
    return request


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "before_record_request": replace_post_body,
    }
