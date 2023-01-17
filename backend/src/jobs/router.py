from src.jobs.schemas import Job, JobBase
from fastapi import status, APIRouter

from src.jobs.crud import job_crud

# from src.jobs import service
from typing import List

router = APIRouter()


@router.get("/job")
async def get_job_by_id(job_id: int):
    return await job_crud.get(job_id)


@router.get("/jobs", response_model=List[JobBase])
async def get_all_jobs(skip: int = 0, limit: int = 100):
    return await job_crud.get_multi(skip, limit)


@router.post("/job", status_code=status.HTTP_201_CREATED, response_model=Job)
async def add_job(job_data: Job):
    return await job_crud.create(job_data.dict())


@router.post("/jobs", status_code=status.HTTP_201_CREATED, response_model=List[Job])
async def add_job_list(job_list: List[Job]):
    return await job_crud.create_multi(job_list)


@router.delete("/job", status_code=status.HTTP_200_OK)
async def del_job(job_id: int):
    await job_crud.remove(job_id)


@router.delete("/jobs", status_code=status.HTTP_200_OK)
async def del_job_list(job_id_list: List[int]):
    await job_crud.remove_multi(job_id_list)


@router.put("/job", status_code=status.HTTP_200_OK)
async def update_job(job: JobBase):
    return await job_crud.update(job.dict())


@router.put("/jobs", status_code=status.HTTP_200_OK)
async def update_job_list(job_list: List[JobBase]):
    return await job_crud.update_multi(job_list)


"""
@router.post("/jobs", status_code=status.HTTP_201_CREATED, response_model=List[Job])
async def add_job_list(job_data_list: List[Job]):
    job_list = await service.create_job_list(job_data_list)
    return job_list



"""
