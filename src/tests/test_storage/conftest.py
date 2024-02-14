import pytest

from storage.user import UserRepository, AbstractUserRepository


@pytest.fixture(scope='function')
def user_repository(manager) -> AbstractUserRepository:
    return UserRepository(manager)
