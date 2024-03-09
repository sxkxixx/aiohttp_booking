from datetime import timedelta

import pytest_asyncio
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient
from aiohttp.web import Response, Request, Application

from common.service import HashService, JWTService
from endpoint.rest.auth import AuthRouter
from infrastructure.config import ApplicationConfig
from main import init_app
from storage.user import UserRepository
from storage.verity_record.pw_verify_record import PWVerifyRecordRepository
from tests.mock_types.publisher import MockPublisher


@pytest_asyncio.fixture(scope='function')
async def app_client(aiohttp_client):
    async def ping(request: Request) -> Response:
        return Response(text='pong')

    app: Application = init_app()
    app.router.add_route('GET', '/', ping)
    yield await aiohttp_client(app)


@pytest_asyncio.fixture(scope='function')
async def auth_app_client(aiohttp_client, manager):
    app = Application()
    auth_router = AuthRouter(
        UserRepository(manager),
        PWVerifyRecordRepository(manager),
        MockPublisher(),
        HashService(),
        JWTService(
            access_token_timedelta=timedelta(minutes=ApplicationConfig.ACCESS_TOKEN_EXPIRE_MINUTES),
            secret_key=ApplicationConfig.SECRET_KEY,
        )
    )
    app.add_subapp('/api/v1/auth', auth_router.setup_router())

    async def ping(request: Request) -> Response:
        return Response(text='pong')

    app.router.add_route('GET', '', ping)
    yield await aiohttp_client(app)


@pytest_asyncio.fixture(scope='function')
async def user_created(auth_app_client: TestClient):
    response: ClientResponse = await auth_app_client.post(
        '/api/v1/auth/register',
        json=dict(email='user@gmail.com', password='password')
    )
    assert response.ok
