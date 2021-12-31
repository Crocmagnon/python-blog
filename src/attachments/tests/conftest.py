from typing import Any, Protocol

import pytest


class Request(Protocol):
    body: Any


def replace_post_body(request: Request) -> Request:
    request.body = None
    return request


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    return {
        "before_record_request": replace_post_body,
    }
