import json
from unittest.mock import MagicMock

import pytest
from sanic.exceptions import NotFound

from src.exceptions import handle_exception


@pytest.mark.asyncio
async def test_handle_not_found_exception():
    request = MagicMock()
    exception = NotFound("Page not found")

    result = await handle_exception(request, exception)
    assert result.status == 200


@pytest.mark.asyncio
async def test_handle_key_error():
    request = MagicMock()
    exception = KeyError("Missing key")

    result = await handle_exception(request, exception)
    result_json = json.loads(result.body)
    assert result.status == 400
    assert result_json == {
        "status": "error",
        "message": "Missing key: 'Missing key' in the request payload.",
    }
