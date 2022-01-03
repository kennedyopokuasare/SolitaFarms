'''
Provides Object Relational Mapping for Database Entities
'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
BaseTable = declarative_base()

class Farm(BaseTable):
    __tablename__='farm'

    id= Column('id',Integer,primary_key=True)
    name=Column('name',String, nullable=False)
    description=Column("description",String)

class SensorType(BaseTable):
    __tablename__='sensor_type'

    id= Column('id',Integer,primary_key=True)
    name=Column('name',String, nullable=False)
    description=Column("description",String)
