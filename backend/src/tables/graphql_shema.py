from pydantic import Field
import strawberry
from strawberry.types import Info
from fastapi import Depends


def custom_context_dependency() -> str:
    return "John"


async def get_context(custom_value=Depends(custom_context_dependency)):
    return {"fdfd": custom_value}


@strawberry.type
class JobReturn:
    id: int
    work_name: str = Field(min_length=1, max_length=200)
    unit_of_measurement: str = Field(min_length=1, max_length=15)


@strawberry.type
class JobCreate:
    work_name: str = Field(min_length=1, max_length=200)
    unit_of_measurement: str = Field(min_length=1, max_length=15)


@strawberry.type
class Query:
    # @strawberry.field
    # async def job(self, job_id: int, info: Info) -> JobReturn:
    # return await job_crud.get(job_id)

    # @strawberry.field
    # async def jobs(self, skip: int = 0, limit: int = 10) -> list[JobReturn]:
    # res = await job_crud.get_multi(skip, limit)
    # res = [JobReturn(**dict(obj._mapping)) for obj in res]
    # return res
    @strawberry.field
    async def exapmle(self, info: Info) -> str:
        return f"Hello {info.context['custom_value']}"


"""
@strawberry.type
class Mutation:
    @strawberry.mutation
    # async def create_job(self, job: JobCreate) -> JobReturn:
    # print(job)
    async def create_job(self, work_name: str, unit_of_measurement: str) -> JobReturn:
        job = {"work_name": work_name, "unit_of_measurement": unit_of_measurement}
        print(job, end="\n")
        res = await job_crud.create(job)
        print(res)
        return {
            "work_name": JobCreate.work_name,
            "unit_of_measurement": JobCreate.unit_of_measurement,
        }


    @strawberry.mutation
    def update_user(
        self, id: int, name: str, email: str, password: str, info: Info
    ) -> str:
        result = conn.execute(
            users.update().where(users.c.id == id),
            {"name": name, "email": email, "password": password},
        )
        print(result.returns_rows)
        return str(result.rowcount) + " Row(s) updated"

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        result = conn.execute(users.delete().where(users.c.id == id))
        return result.rowcount > 0
"""
