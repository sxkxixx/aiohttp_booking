from typing import Any

import pytest
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient

from common.service import JWTService
from infrastructure.config import ApplicationConfig


@pytest.mark.asyncio
async def test_ping_pong(auth_app_client):
    """
    Ping, Pong
    :param auth_app_client:
    :return:
    """
    resp: ClientResponse = await auth_app_client.get('/')
    assert await resp.text() == 'pong'


@pytest.mark.asyncio
async def test_login_no_user(auth_app_client: TestClient):
    """
    User не создан => 404 статус ответа, то есть пользователь не найден
    """
    body = {'email': 'user@gmail.com', 'password': 'password', 'fingerprint': 'any'}
    response: ClientResponse = await auth_app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 404
    text = await response.text()
    assert text == 'User Not Found'


@pytest.mark.asyncio
async def test_login_wrong_password(auth_app_client: TestClient, user_created):
    """
    Тестирование поведения когда пользователь ввёл некорректный пароль
    """
    body = dict(email='user@gmail.com', password='password')
    body['password'] = 'incorrect_password'
    body['fingerprint'] = 'incorrect_fingerprint'
    response: ClientResponse = await auth_app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 400
    text = await response.text()
    assert text == "Passwords don't match"


@pytest.mark.asyncio
async def test_login_upper_case_email(auth_app_client: TestClient):
    body = {'email': 'user@gmail.com', 'password': 'password'}
    await auth_app_client.post('/api/v1/auth/register', json=body)
    body['email'] = 'USER@GMAIL.COM'
    body.update({'fingerprint': 'any'})
    response: ClientResponse = await auth_app_client.post('/api/v1/auth/login', json=body)
    assert response.status == 200, await response.text()
    json_body = await response.json()
    access_token = json_body['access_token']
    payload = JWTService(Any, ApplicationConfig.SECRET_KEY).get_token_payload(access_token)
    assert payload['email'] == 'user@gmail.com'
