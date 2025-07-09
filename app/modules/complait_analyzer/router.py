import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Request

from api.dependencies import UOWComplaitManager
from modules.complait_analyzer.schemas.payload import ComplaitCreation, ComplaitCreationResponse, ChangeComplaitStatus, Complait
from modules.complait_analyzer.service import ComplaitAnalyzerService

from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/complaits", 
            tags=["Жалобы"],
            summary="Получение всех задач")
async def get_tables(uow: UOWComplaitManager) -> list[Complait]:
    instance = await ComplaitAnalyzerService().get_complaits(uow)
    return instance


@router.post("/complaits", 
             tags=["Жалобы"],
             summary="Создание жалобы",
             description="""
## Создание жалобы.
### Входные данные:
*  **text** `str` - Текст жалобы
### Выходные данные:
* Инстанс созданной жалобы
             """)
async def create_complait(complait: ComplaitCreation, request: Request, uow: UOWComplaitManager) -> ComplaitCreationResponse:
    
    client_ip = request.headers.get("x-forwarded-for")
    if not client_ip:
        client_ip = request.client.host
        
    instance = await ComplaitAnalyzerService().create_complait(uow, complait, client_ip)
    return JSONResponse(validation(ComplaitCreationResponse, instance),
                        status_code=status.HTTP_201_CREATED)


@router.delete("/complaits/{id}", 
               tags=["Жалобы"],
               summary="Удаление жалобы по id",
                description="""
## Удаление жалобы.
### Входные данные:
*  **id** `int` - id удаляемой жалобы
### Выходные данные:
* **200 OK** - жалоба успешно удалена
* **400 BAD_REQUEST** - заданной Жалобы не существует
             """)
async def delete_table(id: int, uow: UOWComplaitManager) -> JSONResponse:
    await ComplaitAnalyzerService().delete_task(uow, id)
    return JSONResponse("Жалоба успешно удалена!", status_code=status.HTTP_200_OK)

@router.patch("/change_status/",
               tags=["Жалобы"],
               summary="Изменение статуса жалобы",
                description="""
## Изменение статуса жалобы.
### Входные данные:
*  **id** `int` - id жалобы
*  **status** `str` - статус жалобы
### Выходные данные:
Инстанс жалобы
             """)
async def change_complait_status(data: ChangeComplaitStatus, uow: UOWComplaitManager) -> Complait:
    complait_to_update = await ComplaitAnalyzerService().update_status(uow, data)
    return complait_to_update

@router.get("/actual_complaits",
            tags=["Жалобы"],
            summary="Получение открытых жалоб за псоелдний час")
async def get_actual_complaits(uow: UOWComplaitManager) -> list[Complait]:
    instance = await ComplaitAnalyzerService().get_actual_complaits(uow)
    return instance
