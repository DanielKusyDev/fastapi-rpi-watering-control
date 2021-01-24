import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

Base = declarative_base()


class ModelMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True, index=True)
    add_date = Column(DateTime, default=datetime.datetime.utcnow)


class Plant(ModelMixin, Base):
    __tablename__ = "plants"
    name = Column(String(256), index=True)
    sensors = relationship("Sensor", uselist=True, back_populates="plant", lazy='subquery')


class Sensor(ModelMixin, Base):
    __tablename__ = "sensors"
    name = Column(String(256), index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    plant = relationship("Plant")


class Gpio(Base):
    __tablename__ = "gpios"
    channel = Column(Integer, index=True, unique=True, primary_key=True, autoincrement=False)
    state = Column(Boolean, default=False, nullable=False)
    description = Column(String(1054), nullable=True)
    callback = Column(String(1054), nullable=True)
