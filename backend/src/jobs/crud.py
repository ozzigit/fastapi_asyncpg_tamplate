from src.jobs.schemas import Job, JobUpdate
from src.core.crud import CRUDBase
from src.jobs.models import jobs


class CRUDJob(CRUDBase[jobs, Job, JobUpdate]):
    pass


job_crud = CRUDJob(jobs)
