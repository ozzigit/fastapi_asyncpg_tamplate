from sqlalchemy import (
    # Boolean,
    Column,
    # DateTime,
    # ForeignKey,
    Identity,
    Integer,
    # LargeBinary,
    MetaData,
    String,
    Table,
    # func,
)
# from sqlalchemy import UniqueConstraint


from src.core.constants import DB_NAMING_CONVENTION
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

jobs = Table(
    "jobs",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("work_name", String, nullable=False),
    Column("unit_of_measurement", String, nullable=False),
    # UniqueConstraint("work_name", "unit_of"),
)
