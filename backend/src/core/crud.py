from typing import Generic, List, Type, TypeVar
from sqlalchemy import select, insert, delete, update
from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from src.core.db import database
from src.core.exceptions import RowIsPresent, NotFound, BadRequest
from src.core.models import ORJSONModel as Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], create_shema, update_shema):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.create_shema = create_shema
        self.update_shema = update_shema

    async def get(self, id_obj: int, limit: int) -> List[ModelType]:
        if limit is None:
            get_query = select(self.model).where(self.model.c.id == id_obj)
            obj = await database.fetch_one(get_query)
            if not obj:
                err = NotFound
                err.DETAIL += f" id {id_obj}"
                raise err
            return [obj]
        else:
            select_query = (
                select(self.model)
                .offset(id_obj - 1)
                .limit(limit)
                .order_by(self.model.c.id)
            )
            return await database.fetch_all(select_query)

    async def create(self, list_obj: List[CreateSchemaType]):
        if len(list_obj) == 1:
            # print(*jsonable_encoder(list_obj[0]))
            insert_query = (
                insert(self.model).values(list_obj[0].dict()).returning(self.model)
            )
            try:
                return await database.fetch_one(insert_query)
            except UniqueViolationError:
                err = RowIsPresent
                err.DETAIL += f" {list_obj[0].dict()}"
                raise err

        elif len(list_obj) > 1:
            try:
                insert_query = (
                    insert(self.model)
                    .values([obj.dict() for obj in list_obj])
                    .returning(self.model)
                )
                return await database.fetch_all(insert_query)
            except UniqueViolationError:
                err = RowIsPresent
                raise err
        else:
            raise BadRequest

    async def remove(self, id_list: List[int]) -> List[ModelType]:
        if len(id_list) == 1:
            del_query = (
                delete(self.model)
                .where(self.model.c.id == id_list[0])
                .returning(self.model.c.id)
            )
            res = await database.fetch_one(del_query)
            return [res]
        elif len(id_list) > 1:
            del_job_list_query = (
                delete(self.model)
                .where(self.model.c.id.in_(id_list))
                .returning(self.model.c.id)
            )
            return await database.fetch_all(del_job_list_query)
        else:
            raise BadRequest

    async def _update(self, obj: UpdateSchemaType) -> ModelType:
        update_query = (
            update(self.model)
            .where(self.model.c.id == obj["id"])
            .values(obj)
            .returning(self.model)
        )
        try:
            return await database.fetch_one(update_query)
        except UniqueViolationError:
            raise RowIsPresent

    async def update(self, list_obj: List[UpdateSchemaType]):
        # bad variant
        response = []
        for obj in list_obj:
            response.append(await self._update(obj.dict()))
        return response
