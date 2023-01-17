from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import select, insert, delete, update
from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from src.core.db import database

from src.core.exceptions import RowIsPresent
from src.core.models import ORJSONModel as Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        get_query = select(self.model).where(self.model.c.id == id)
        return await database.fetch_one(get_query)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:

        select_query = (
            select(self.model).offset(skip).limit(limit).order_by(self.model.c.id)
        )
        return await database.fetch_all(select_query)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        insert_query = insert(self.model).values(obj_in).returning(self.model)
        try:
            return await database.fetch_one(insert_query)
        except UniqueViolationError:
            raise RowIsPresent

    async def create_multi(self, list_obj_in: List[CreateSchemaType]):

        try:
            insert_query = (
                insert(self.model)
                .values([job_el.dict() for job_el in list_obj_in])
                .returning(self.model)
            )
            return await database.fetch_all(insert_query)
        except UniqueViolationError:
            raise RowIsPresent

    async def remove(self, id: int) -> ModelType:
        del_query = delete(self.model).where(self.model.c.id == id)
        return await database.fetch_one(del_query)

    async def remove_multi(self, id_list: List[id]):
        del_job_list_query = delete(self.model).where(self.model.c.id.in_(id_list))
        return await database.fetch_all(del_job_list_query)

    async def update(
        self, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        update_query = (
            update(self.model)
            .where(self.model.c.id == obj_in["id"])
            .values(obj_in)
            .returning(self.model)
        )
        try:
            return await database.fetch_one(update_query)
        except UniqueViolationError:
            raise RowIsPresent

    async def update_multi(
        self, list_obj_in: List[Union[UpdateSchemaType, Dict[str, Any]]]
    ):
        # bad variant
        response = []
        for obj in list_obj_in:
            response.append(await self.update(obj.dict()))
        return response
