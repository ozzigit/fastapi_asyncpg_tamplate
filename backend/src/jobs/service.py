from databases.interfaces import Record
from sqlalchemy import insert, select, and_
from asyncpg.exceptions import UniqueViolationError
from src.jobs.exceptions import RowIsPresent
from src.jobs.schemas import Job
from src.core.db import database
from src.jobs.models import jobs

from typing import List


async def create_job_list(job_list: List[Job]):
    try:
        insert_query = (
            insert(jobs).values([job_el.dict() for job_el in job_list]).returning(jobs)
        )
        return await database.fetch_all(insert_query)
    except UniqueViolationError:
        for job_in_query in job_list:
            if await get_job(job_in_query):
                raise RowIsPresent


async def get_job(job: Job) -> Record | None:
    select_query = select(jobs).where(
        and_(
            jobs.c.work_name == job.work_name,
            jobs.c.unit_of_measurement == job.unit_of_measurement,
        )
    )  # UniqueConstraint check

    return await database.fetch_one(select_query)
