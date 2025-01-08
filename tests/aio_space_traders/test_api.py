from unittest.mock import patch, AsyncMock

import pytest
from aio_space_traders.api import SpaceTraders
from aio_space_traders.errors import SpaceTradersAPIError
from tests import factories

@pytest.mark.asyncio
@patch("niquests.AsyncSession.request", new_callable=AsyncMock)
async def test_get_status_successful_with_token(niquests_mock: AsyncMock):
    mock_data = factories.ServerStatusResponseFactory.build()
    mock_response = AsyncMock()
    mock_response.ok = True
    mock_response.json.return_value = mock_data.model_dump()

    niquests_mock.return_value = mock_response

    api = SpaceTraders(token="test_token")
    response = await api.get_status()
    assert response.status == mock_data.status

@pytest.mark.asyncio
@patch("niquests.AsyncSession.request", new_callable=AsyncMock)
async def test_get_status_successful_without_token(niquests_mock: AsyncMock):
    mock_data = factories.ServerStatusResponseFactory.build()
    mock_response = AsyncMock()
    mock_response.ok = True
    mock_response.json.return_value = mock_data.model_dump()

    niquests_mock.return_value = mock_response

    api = SpaceTraders()
    response = await api.get_status()
    assert response.status == mock_data.status

@pytest.mark.asyncio
@patch("niquests.AsyncSession.request", new_callable=AsyncMock)
async def test_get_status_failure(niquests_mock: AsyncMock):
    mock_response = AsyncMock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.json = AsyncMock(return_value={
        "error": {
            "code": 500,
            "message": "Internal Server Error",
        },
    })

    niquests_mock.return_value = mock_response

    api = SpaceTraders(token="test_token")

    with pytest.raises(SpaceTradersAPIError) as exc_info:
        await api.get_status()

    assert "Internal Server Error" in str(exc_info.value)

