from typing import Any

import pytest
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient

from infrastructure.config import ApplicationConfig
from service import JWTService


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
async def test_login_no_user(app_client: TestClient):
    """
    User не создан => 404 статус ответа, то есть пользователь не найден
    """
    body = {'email': 'user@gmail.com', 'password': 'password', 'fingerprint': 'any'}
    response: ClientResponse = await app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 404
    text = await response.text()
    assert text == 'User Not Found'


@pytest.mark.asyncio
async def test_login_wrong_password(app_client: TestClient, user_created, user):
    """
    Тестирование поведения когда пользователь ввёл некорректный пароль
    """
    body = user.copy()
    body['password'] = 'incorrect_password'
    body['fingerprint'] = 'incorrect_fingerprint'
    response: ClientResponse = await app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 400
    text = await response.text()
    assert text == "Passwords don't match"


@pytest.mark.asyncio
async def test_login_upper_case_email(app_client: TestClient):
    body = {'email': 'user@gmail.com', 'password': 'password'}
    await app_client.post('/api/v1/auth/register', json=body)
    body['email'] = 'USER@GMAIL.COM'
    body.update({'fingerprint': 'any'})
    response: ClientResponse = await app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 200, await response.text()
    json_body = await response.json()
    access_token = json_body['access_token']
    payload = JWTService(Any, ApplicationConfig.SECRET_KEY).get_token_payload(access_token)
    assert payload['email'] == 'user@gmail.com'
