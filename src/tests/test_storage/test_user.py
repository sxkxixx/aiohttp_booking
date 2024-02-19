from typing import Optional

import peewee
import pytest

from dto.user import UserRegisterRequest
from infrastructure.database.model import User
from storage.user import AbstractUserRepository

USER = UserRegisterRequest(email='user@gmail.com', password='password')


@pytest.mark.asyncio
async def test_user_creating(user_repository: AbstractUserRepository):
    """Создает пользователя и проверяет наличие записи в БД"""
    await user_repository.create_user(USER)
    user: Optional[User] = await user_repository.get_user(User.email == 'user@gmail.com')
    assert user is not None
    assert user.email == 'user@gmail.com'


@pytest.mark.asyncio
async def test_user_deleting(user_repository: AbstractUserRepository):
    """
    Простой тест на проверку, что данных в таблице нет
    :param user_repository:
    :return:
    """
    user: Optional[User] = await user_repository.get_user(User.email == 'user@gmail.com')
    assert not user


@pytest.mark.asyncio
async def test_user_raises_integrity_error(user_repository: AbstractUserRepository):
    """
    Проверяет, что будет выброшена ошибке, если создан пользователь с таким же email
    :param user_repository:
    :return:
    """
    await user_repository.create_user(USER)

    with pytest.raises(peewee.IntegrityError):
        await user_repository.create_user(USER)
