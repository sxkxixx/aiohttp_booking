import pytest
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient


@pytest.mark.asyncio
async def test_ping_pong(app_client):
    """
    Ping, Pong
    :param app_client:
    :return:
    """
    resp: ClientResponse = await app_client.get('/')
    assert await resp.text() == 'pong'


@pytest.mark.asyncio
async def test_login(app_client: TestClient, user_created, user):
    resp: ClientResponse = await app_client.post('/api/v1/auth/login', json=user)
    assert resp.ok
    json: dict = await resp.json()
    assert json['token_type'] == 'Bearer'
    assert json['header'] == 'Authorization'
    cookies = resp.cookies
    assert cookies['refresh_token'] == 'refresh_token'
