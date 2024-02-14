import pytest
import pytest_asyncio
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient
from aiohttp.web import Response, Request, Application

from dto.user import UserAuthRequest
from main import init_app


@pytest_asyncio.fixture
async def app_client(aiohttp_client):
    async def ping(request: Request) -> Response:
        return Response(text='pong')

    app: Application = init_app()
    app.router.add_route('GET', '/', ping)
    yield await aiohttp_client(app)


@pytest.fixture(scope='session')
def user() -> dict[str, str]:
    return dict(email='user@gmail.com', password='password')


@pytest_asyncio.fixture(scope='function')
async def user_created(app_client: TestClient, user: dict[str, str]):
    response: ClientResponse = await app_client.post(
        '/api/v1/auth/register',
        json=user
    )
    assert response.ok
