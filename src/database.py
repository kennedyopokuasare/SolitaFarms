'''
Provides the database API to access the application data
'''
from sqlalchemy import create_engine,MetaData, Table, Column, Integer, String
from .entities import BaseTable,SensorData, SensorType, Farm
from sqlalchemy.orm import sessionmaker
import pandas as pd
import glob

DEFAULT_DB_PATH='data/db/solitafarms.db'
DEFAULT_DATA_PATH="data/external/"

class Engine(object):
    '''
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file.
    
    :param db_path: The path for the database file
    
    '''

    def __init__(self,db_path=None):
        super(Engine,self).__init__()
        if db_path is not None:
            self.db_path=db_path
        else:
            self.db_path=DEFAULT_DB_PATH

        self.dbengine=create_engine('sqlite:///'+self.db_path)


    def get_dbEngine(self):
        if self.dbengine is None:
            self.dbengine=create_engine('sqlite:///'+self.db_path)
        return self.dbengine

    def get_dbSession(self):
        Session=sessionmaker(bind=self.get_dbEngine())
        self.dbSession=Session()

    def remove_database(self):
        engine=self.get_dbEngine()
        BaseTable.metadata.drop_all(engine)
    

    def create_tables(self):
        '''
        Create dabatabase tables using Object Relational Mapping
        '''
        engine=self.get_dbEngine()
        BaseTable.metadata.create_all(engine)

    def populate_tables(self,data_path=None):
        '''
        Read, validate and populate the database with csv data
        :param data_path: The path to the directory for the csv data
        '''
        if data_path is None:
            data_path=DEFAULT_DATA_PATH

        # read and concatinate all csv data
        all_data_files=glob.glob(data_path+"*.csv")

        raw_dataset=pd.concat([
                    pd.read_csv(filename,index_col=None,parse_dates=["datetime"]) 
                    for filename in all_data_files
                ],axis=0,ignore_index=True)
                
        # Accept only temperature,rainfall and PH data
        metrics={
                        "temperature":SensorType(name="temperature",description="Temperature sensor"),
                        "pH":SensorType(name="pH", description="pH sensor"),
                        "rainFall":SensorType(name="rainFall",description="RainFall sensor")
                        }
        raw_dataset=raw_dataset[raw_dataset.sensorType.isin(metrics.keys())]
        
        
        #Data may be missing from certain dates
        #validate for all missing columns as well
        raw_dataset=raw_dataset[~raw_dataset.isnull().any(axis=1)]
    
        #All farms
        farms={entry.strip():Farm(name=entry.strip()) for entry in raw_dataset["location"].unique().tolist()}

        # pH is a decimal value between 0 - 14
        ph_validated=raw_dataset[(raw_dataset.sensorType=="pH") & (raw_dataset.value.between(0,14))]

        #Temperature is a celsius value between -50 and 100
        temperature_validated=raw_dataset[(raw_dataset.sensorType=="temperature") & 
                    (raw_dataset.value.between(-50,100))]

        #Rainfall is a positive number between 0 and 500
        rainfall_validated=raw_dataset[(raw_dataset.sensorType=="rainFall") & 
                    (raw_dataset.value.between(0,500))]

        #Final validated dataset 
        validated_dataset=[
                SensorData(
                    sensor_type=metrics[entry["sensorType"].strip()],
                    farm=farms[entry["location"].strip()],
                    date=entry["datetime"],
                    value=entry["value"]
                )  
                for _,entry in pd.concat([
                                            ph_validated,
                                            rainfall_validated,
                                            temperature_validated
                                        ],
                                        axis=0,ignore_index=True).iterrows()]
        
        
        #insert data into database
        
        self.get_dbSession()
        self.dbSession.add_all(validated_dataset)
        self.dbSession.commit()

        

