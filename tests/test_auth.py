import pytest
import respx
import httpx
from datetime import datetime
from auth.token_manager import TokenManager
from config.settings import settings

@pytest.fixture
def token_manager():
    return TokenManager()

@pytest.mark.asyncio
@respx.mock
async def test_issue_token_success(token_manager):
    # Mocking au10001 endpoint
    url = f"{settings.kiwoom_api_host}/oauth2/token"
    mock_response = {
        "access_token": "mock_access_token_12345",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    respx.post(url).mock(return_value=httpx.Response(200, json=mock_response))

    token = await token_manager.issue_token()
    
    assert token == "mock_access_token_12345"
    assert token_manager._access_token == "mock_access_token_12345"
    assert token_manager._expires_at is not None
    assert token_manager._expires_at > datetime.now()

@pytest.mark.asyncio
@respx.mock
async def test_issue_token_failure(token_manager):
    url = f"{settings.kiwoom_api_host}/oauth2/token"
    respx.post(url).mock(return_value=httpx.Response(401, json={"error": "invalid_client"}))

    with pytest.raises(httpx.HTTPStatusError):
        await token_manager.issue_token()
