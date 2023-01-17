from src.core.exceptions import BadRequest


class RowIsPresent(BadRequest):
    DETAIL = "Row is already exist in table"
