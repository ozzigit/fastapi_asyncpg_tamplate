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
    UniqueConstraint,
)


from src.core.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

jobs = Table(
    "jobs",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("work_name", String(200), nullable=False),
    Column("unit_of_measurement", String(15), nullable=False),
    UniqueConstraint("work_name", "unit_of_measurement"),
)
