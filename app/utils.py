from typing import List, Any, Union, Annotated, Optional, Tuple

from fastapi import Response, HTTPException, status
from aiohttp.client_exceptions import ClientResponseError
import aiohttp

from loguru import logger
from pydantic import BaseModel


def validation(
        validation_model: BaseModel,
        instance_object: Union[List, Any, None]) -> Union[List[dict], dict]:
    """
    Функция для валидации объектов по заданной pydantic-схеме
    """
    try:
        if isinstance(instance_object, list):
            return [
                validation_model.model_validate(
                    instance, from_attributes=True).model_dump()
                for instance in instance_object
            ]
        elif instance_object is None:
            return {"detail": "no data provided due to status code"}
        else:
            return validation_model.model_validate(
                instance_object, from_attributes=True).model_dump()
    except Exception as e:
        logger.error(f"Validation error occured, {e}")
        return {"detail": "error occured"}
    
async def post_data(url: str,
                    headers: Optional[dict] = None,
                    data: Optional[Union[str, dict]] = None,
                    json: Optional[dict] = None,
                    params: Optional[Tuple[str, Any]] = None,
                    *args,
                    **kwargs) -> Response:
    try:
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=60, connect=3)
            async with session.post(url,
                                    data=data,
                                    headers=headers,
                                    timeout=timeout,
                                    json=json,
                                    params=params,
                                    **kwargs) as response:
                result = await response.json()
                response.raise_for_status()
                # data = await response.text()
                return result.get("sentiment", "unknown")
    except ClientResponseError as e:
        logger.error(f"Ошибка запроса POST: \n{e}")
        logger.warning("Поставленная тональность - unknown")
        return "unknown"
    except AttributeError as e:
        logger.error(f"Ошибка запроса POST: \n{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Неизвестная ошибка сервера")
    except TimeoutError as e:
        logger.error(f"Время ожидания вышло")
        logger.warning("Поставленная тональность - unknown")
        return "unknown"
    except Exception as e:
        raise e
    
async def fetch_data(url: str,
                    params: Optional[Tuple[str, Any]] = None
                     ) -> Response:
    try:
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=60, connect=3)
            async with session.get(url, 
                                   timeout=timeout,
                                    params=params,

                                   ) as response:
                response.raise_for_status()
                data = await response.json()
                return data
    except ClientResponseError as e:
        logger.error(e)
        error_detail = data.get("detail", data) if isinstance(
            data, dict) else "Незвестная ошибка сервера"
        raise HTTPException(status_code=e.status, detail=error_detail)
    except AttributeError as e:
        logger.error(f"Ошибка запроса GET: \n{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Неизвестная ошибка сервера")
    except Exception as e:
        raise e
