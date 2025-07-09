import json
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from unitofwork import AbstractUnitOfWork
from modules.complait_analyzer.schemas.payload import ComplaitCreation, Status, ChangeComplaitStatus
from api.dependencies import UOWComplaitManager
from modules.external_apis.category_analyzer import CategoryAnalyzer
from modules.external_apis.geolocation_api import GeolocationFinder
from modules.external_apis.sentiment_analyzer import SentimentAnalyzer


class ComplaitAnalyzerService:
    
    async def get_complaits(self, uow: AbstractUnitOfWork):
        logger.info(
            "\n\tПолучение списка обращений"
            )
        async with uow:
            try:
                complaits = await uow.complaits.get_all()
                logger.success(
                    "\n\tжалоб: \n"
                    f"\t {complaits}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка жалоб: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка жалоб")
            return complaits
    
    async def create_complait(self, uow: AbstractUnitOfWork, complait_data: ComplaitCreation, client_ip: str):
        category_analyzer = CategoryAnalyzer()
        geolocation_finder = GeolocationFinder()
        sentiment_analyzer = SentimentAnalyzer()
        
        data = complait_data.model_dump(exclude={'id'})
        logger.info(
            f"\n\tСоздание жалобы:"
            f"{data}"
        )
        text = data.get("text")
        geolocation = await geolocation_finder.get_geolocation(client_ip)
        category = await category_analyzer.get_category(text)
        sentiment = await sentiment_analyzer.get_sentimentality(text)
        async with uow:
            try:
                task = await uow.complaits.create(
                    {
                        "text": text,
                        "sentiment": sentiment,
                        "geolocation": json.dumps(geolocation),
                        "category": category
                    }
                    )
                await uow.commit()
                logger.success(f"Обращение успешно создано!")
            except ValueError as e:
                await uow.rollback()
                logger.error(f"Обращение уже существует!")
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Обращение уже существует!")
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при создании обращения: {str(e)}")
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Ошибка при валидации данных")
            return task
        
    async def delete_task(self, uow: AbstractUnitOfWork, complait_id: int):
        async with uow:
            try:
                await uow.complaits.delete(uow.complaits.model.id == complait_id)
                await uow.commit()
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Обращение с id '{complait_id}' не существует!")
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Обращения с id '{complait_id}' не существует!")
            except Exception as e:
                await uow.rollback()
                logger.error(
                    f"Ошибка при удалении стола: {e}"
                    )
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при удалении обращения")
            
    async def update_status(self, uow: AbstractUnitOfWork, data: ChangeComplaitStatus):
        complait_id = data.id
        name = "status"
        complait_status = data.status.value
        logger.debug(
            f"\n\tИзменение статуса жалоби с id: {complait_id}\n"
            f"\n\tСтатус: {complait_status}\n"
        )
        async with uow:
            try:
                complate_to_update = await uow.complaits.update(name, complait_status, uow.complaits.model.id == complait_id)
                if not complate_to_update:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Жалоба не найдена")
                await uow.commit()
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при изменении статуса жалобы: {e}")
                raise e
            return complate_to_update
        
    async def get_actual_complaits(self, uow: AbstractUnitOfWork):
        logger.info(
            "\n\tПолучение списка жалоб"
            )
        async with uow:
            try:
                status_filter = (uow.complaits.model.status == "open")
                one_hour_ago = datetime.now() - timedelta(hours=1)
                last_hour_filter = (uow.complaits.model.timestamp >= one_hour_ago)
                complaits = await uow.complaits.filter(and_(status_filter, last_hour_filter))
                logger.success(
                    "\n\tЖалобы: \n"
                    f"\t {complaits}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка жалоб: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка жалоб")
            return complaits



