from sqlalchemy import (
    Column,
    DateTime,
    func
)


class TimestampColumns(object):
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(),
                     onupdate=func.now())


class CreatedColumn(object):
    created = Column(DateTime, default=func.now())
