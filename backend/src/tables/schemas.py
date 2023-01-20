from pydantic import Field
from typing import List

from src.core.models import ORJSONModel


class Id(ORJSONModel):
    id: int | List[int]


# Properties to return to client
class JobInput(ORJSONModel):
    work_name: str = Field(min_length=1, max_length=200)
    unit_of_measurement: str = Field(min_length=1, max_length=15)


# Properties shared by models stored in DB
class JobBase(ORJSONModel):
    id: int
    work_name: str = Field(min_length=1, max_length=200)
    unit_of_measurement: str = Field(min_length=1, max_length=15)

    class Config:
        orm_mode: True


class JobUpdate(JobBase):
    pass


# Properties to return to client
class ObjInput(ORJSONModel):
    adress: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=15)


# Properties shared by models stored in DB
class ObjBase(ORJSONModel):
    id: int
    adress: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=15)

    class Config:
        orm_mode: True


# Properties to input to client
class ObjUpdate(JobBase):
    pass


# Properties to return to client
class WorkerInput(ORJSONModel):
    name: str = Field(min_length=1, max_length=100)
    speciality: str = Field(min_length=1, max_length=15)


# Properties shared by models stored in DB
class WorkerBase(ORJSONModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    speciality: str = Field(min_length=1, max_length=15)

    class Config:
        orm_mode: True


# Properties to input to client
class WorkerUpdate(JobBase):
    pass
