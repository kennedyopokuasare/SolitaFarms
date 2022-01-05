'''
Provides Object Relational Mapping and Database Entities
'''
from sqlalchemy import Column,ForeignKey, Integer,DateTime, String,Numeric
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta

BaseTable = declarative_base()


class JsonifiableBase(object):
    def to_dict(self):
        return {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}
    def __iter__(self):
        return self.to_dict().iteritems()

class Farm(JsonifiableBase,BaseTable):
    __tablename__='farm'

    id= Column('id',Integer,primary_key=True)
    name=Column('name',String, nullable=False)
    description=Column("description",String)

class SensorType(JsonifiableBase,BaseTable):
    __tablename__='sensor_type'

    id= Column('id',Integer,primary_key=True)
    name=Column('name',String, nullable=False,)
    description=Column("description",String)

class SensorData(JsonifiableBase,BaseTable):
    __tablename__="sensor_data"

    id=Column('name',Integer,primary_key=True)
    farm_id=Column('farm_id',Integer,ForeignKey('farm.id'))
    sensor_type_id=Column("sensor_type_id",Integer,ForeignKey('sensor_type.id'))
    date=Column("date",DateTime, nullable=False)
    value=Column("value",Numeric, nullable=False)

    sensor_type=relationship("SensorType",back_populates="sensor_data")
    farm=relationship("Farm",back_populates="sensor_data")

Farm.sensor_data=relationship("SensorData",order_by="desc(SensorData.date)",back_populates="farm")
SensorType.sensor_data=relationship("SensorData",order_by="desc(SensorData.date)",back_populates="sensor_type")