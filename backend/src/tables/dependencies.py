from src.core.exceptions import BadRequest
from src.tables.crud import tables_crud


async def valid_table_name(table_name: str) -> str:
    if table_name not in tables_crud:
        raise BadRequest

    return table_name


async def valid_obj_id(obj_id: int):
    if obj_id < 1:
        raise BadRequest

    return obj_id
