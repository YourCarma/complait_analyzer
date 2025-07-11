from typing import Annotated

from fastapi import Depends

from unitofwork import AbstractUnitOfWork
from modules.complait_analyzer.uow import ComplaitUnitofWork

UOWComplaitManager = Annotated[AbstractUnitOfWork, Depends(ComplaitUnitofWork)]
