'''
Provides the database API to access the application data
'''
from sqlalchemy import create_engine,MetaData, Table, Column, Integer, String
from .entities import BaseTable

DEFAULT_DB_PATH='data/db/solitafarms.db'

class Engine(object):
    '''
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file.
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
            self.dbengine=sam.create_engine('sqlite:///'+self.db_path)
        return self.dbengine

    def remove_database(self):
        pass
    def create_tables(self):
        '''
        Create dabatabase tables using Object Relational Mapping
        '''
        engine=self.get_dbEngine()
        BaseTable.metadata.create_all(engine)

    def populate_tables(self,data_path=None):
        pass