from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now


class BaseModelCls:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True, index=True)
    add_date = Column(DateTime, default=now)


Base = declarative_base(cls=BaseModelCls)


class Plant(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    sensor = relationship("Sensor", uselist=False, back_populates="plant")


class Sensor(Base):
    name = Column(String(256), index=True)
    plant_id = Column(Integer, ForeignKey("plant.id"))
    plant = relationship("Plant", back_populates="sensor")


class GpioInput(Base):
    pin = Column(Integer, index=True, unique=True)
    state = Column(Boolean, default=False)
