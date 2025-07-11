from database.connection import async_session_maker
from loguru import logger
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import OperationalError

from modules.complait_analyzer.models import *
from database.repository import DatabaseRepository
from unitofwork import AbstractUnitOfWork
from exceptions import ServiceUnavailable
from settings import settings


class ComplaitUnitofWork(AbstractUnitOfWork):

    def __init__(self):
        super().__init__()
        self.session = None

    async def __aenter__(self):
        try:
            self.session = self.factory()
            self.complaits = DatabaseRepository(Complaits, self.session)
        except OperationalError as e:
            logger.error(
                "Ошибка подключения к СУБД!"
                f"Проверьте подключение по адресу: {settings.DB_URL}"
                )
            raise ServiceUnavailable(
                "База данных"
            )
        
    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()