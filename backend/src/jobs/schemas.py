from pydantic import Field

from src.core.models import ORJSONModel


# Properties to return to client
class Job(ORJSONModel):
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
