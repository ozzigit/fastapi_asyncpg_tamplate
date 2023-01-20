from fastapi import status, APIRouter, Depends
from typing import List

# from fastapi.encoders import jsonable_encoder
from src.tables.dependencies import valid_table_name, valid_obj_id
from src.tables.crud import tables_crud

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/existing_tables")
def get_tables_list():
    return list(tables_crud.keys())


@router.get(
    "/{table_name}",
    status_code=status.HTTP_200_OK,
)
async def get_obj(
    obj_id: int = Depends(valid_obj_id),
    table_name: str = Depends(valid_table_name),
    limit: int | None = None,
):
    return await tables_crud[table_name].get(obj_id, limit)


@router.delete("/{table_name}", status_code=status.HTTP_200_OK)
async def del_obl(
    obj_list: List[int] = [], table_name: str = Depends(valid_table_name)
):
    return await tables_crud[table_name].remove(obj_list)


for table in tables_crud:

    @router.post(
        f"/{table}",
        status_code=status.HTTP_201_CREATED,
    )
    async def add_obj(
        obj_list: List[tables_crud[table].create_shema], table_name: str = table
    ):
        return await tables_crud[table_name].create(obj_list)

    @router.put(f"/{table}", status_code=status.HTTP_200_OK)
    async def update_job_list(
        obj_list: List[tables_crud[table].update_shema], table_name: str = table
    ):
        return await tables_crud[table_name].update(obj_list)
