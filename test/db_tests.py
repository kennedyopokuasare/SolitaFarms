import unittest
from src import database

DB_PATH = 'data/db/solitaFarms_test.db'
dbEngine = database.Engine(DB_PATH)


class DatabaseTESTCase(unittest.TestCase):
    '''
    Test cases for the Database 
    '''

    @classmethod
    def setUpClass(cls):
        ''' Creates and the test sqlite database. Removes first any preexisting
            database file
        '''
        print ("Testing {}".format( cls.__name__))
        
        print ('\tRemoving old database if any ...')
        dbEngine.remove_database()

        print('\tCreating database ...')
        dbEngine.create_tables() 

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print ("Testing ENDED for {}".format( cls.__name__))
        dbEngine.remove_database() 

    def setUp(self):
        '''
        Populates the database
        '''
       
        dbEngine.populate_tables()
        self.dbSession=dbEngine.get_dbSession()
    
    def tearDown(self):
        '''
        Close database session and remove all records.
        '''
        self.dbSession.close()
        dbEngine.clear_records()
    
    def test_farm_table_created(self):
        '''
            Check that Farms table is created and populated
        '''
        print ('\n(' + self.test_farm_table_created.__name__ + ')', \
            self.test_farm_table_created.__doc__)
        
    def test_sensor_table_created(self):
        '''
            Check that Sensor table is created and populated
        '''
        print ('\n(' + self.test_sensor_table_created.__name__ + ')', \
            self.test_sensor_table_created.__doc__)

    def test_sensor_data_date_is_valid(self):
        '''
            Check that Sensor data date is not None
        '''
        print ('\n(' + self.test_sensor_data_date_is_valid.__name__ + ')', \
            self.test_sensor_data_date_is_valid.__doc__)

    def test_ph_values_are_valid(self):
        '''
            Check that pH values are between 0 - 14
        '''
        print ('\n(' + self.test_ph_values_are_valid.__name__ + ')', \
            self.test_ph_values_are_valid.__doc__)

    def test_temperature_values_are_valid(self):
        '''
            Check that temperature values are between -50 and 100
        '''
        print ('\n(' + self.test_temperature_values_are_valid.__name__ + ')', \
            self.test_temperature_values_are_valid.__doc__)

    def test_metrics_types_are_valid(self):
        '''
            Check that metric types are only temperature,rainfall and pH
        '''
        print ('\n(' + self.test_metrics_types_are_valid.__name__ + ')', \
            self.test_metrics_types_are_valid.__doc__)


if __name__ == '__main__':
    print ('Started running Database tests')
    unittest.main()