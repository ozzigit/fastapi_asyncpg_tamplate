from src.tables import schemas
from src.core.crud import CRUDBase
from src.tables.models import job_tb, object_tb, workers_tb

# if needed to reload methods


class CRUDJob(CRUDBase[job_tb, schemas.JobInput, schemas.JobUpdate]):
    pass


class CRUDObject(CRUDBase[object_tb, schemas.ObjInput, schemas.ObjUpdate]):
    pass


class CRUDWorkers(CRUDBase[workers_tb, schemas.WorkerInput, schemas.WorkerUpdate]):
    pass


tables_crud = {
    job_tb.name: CRUDJob(job_tb, schemas.JobInput, schemas.JobUpdate),
    object_tb.name: CRUDObject(object_tb, schemas.ObjInput, schemas.ObjUpdate),
    workers_tb.name: CRUDWorkers(workers_tb, schemas.WorkerInput, schemas.WorkerUpdate),
}
