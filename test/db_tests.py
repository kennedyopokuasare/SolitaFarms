import unittest
from src import database

DB_PATH = 'data/db/solitafarms_test.db'
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
        print("Testing {}".format(cls.__name__))

        print('\tRemoving old database if any ...')
        dbEngine.remove_database()

        print('\tCreating database ...')
        dbEngine.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print("Testing ENDED for {}".format(cls.__name__))
        dbEngine.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        dbEngine.populate_tables()
        self.dbSession = dbEngine.get_dbSession()

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
        print('\n(' + self.test_farm_table_created.__name__ + ')',
              self.test_farm_table_created.__doc__)

        print("\t Asserting that Farm table is created")
        results = self.dbSession.execute("SELECT * FROM farm").all()
        self.assertIsNotNone(results)

        print("\t Asserting that Farm table is populated")
        self.assertGreater(len(results), 0)

        print("\t Asserting that populated Farm table has a name column")
        self.assertIn("name", results[0].keys())

    def test_sensor_table_created(self):
        '''
            Check that Sensor table is created and populated
        '''
        print('\n(' + self.test_sensor_table_created.__name__ + ')',
              self.test_sensor_table_created.__doc__)

        print("\t Asserting that Sensor table is created")
        results = self.dbSession.execute("SELECT * FROM sensor_data").all()
        self.assertIsNotNone(results)

        print("\t Asserting that Sensor table is populated")
        self.assertGreater(len(results), 0)

        print("\t Asserting that populated Sensor table has a value column")
        self.assertIn("value", results[0].keys())

    def test_sensor_data_date_is_valid(self):
        '''
            Check that Sensor data date is not None
        '''
        print('\n(' + self.test_sensor_data_date_is_valid.__name__ + ')',
              self.test_sensor_data_date_is_valid.__doc__)

        print("\t Asserting that Sensor data date values are not None")
        results = self.dbSession.execute(
            "SELECT date FROM sensor_data WHERE date is NULL").all()

        self.assertEqual(len(results), 0)

    def test_ph_values_are_valid(self):
        '''
            Check that pH values are between 0 - 14
        '''
        print('\n(' + self.test_ph_values_are_valid.__name__ + ')',
              self.test_ph_values_are_valid.__doc__)

        print("\t Asserting that pH sensor data values are between 0 - 14")

        sql = "SELECT sensor_data.value from sensor_data \
             INNER join sensor_type ON sensor_data.sensor_type_id==sensor_type.id\
             WHERE ((sensor_type.name=='pH') AND (sensor_data.value<0 OR sensor_data.value>14))"

        results = self.dbSession.execute(sql).all()

        self.assertEqual(len(results), 0)

    def test_temperature_values_are_valid(self):
        '''
            Check that temperature values are between -50 and 100
        '''
        print('\n(' + self.test_temperature_values_are_valid.__name__ + ')',
              self.test_temperature_values_are_valid.__doc__)

        print("\t Asserting that temperature sensor data values are between -50 - 100")

        sql = "SELECT sensor_data.value from sensor_data \
             INNER join sensor_type ON sensor_data.sensor_type_id==sensor_type.id\
             WHERE ((sensor_type.name=='temperature') AND (sensor_data.value<-50 OR sensor_data.value>100))"

        results = self.dbSession.execute(sql).all()
        self.assertEqual(len(results), 0)

    def test_metrics_types_are_valid(self):
        '''
            Check that metric types are only temperature,rainFall and pH
        '''
        print('\n(' + self.test_metrics_types_are_valid.__name__ + ')',
              self.test_metrics_types_are_valid.__doc__)
        valid_metrics = ["temperature", "rainFall", "pH"]

        print("\t Asserting that there are on 3 metric types")
        results = self.dbSession.execute("SELECT name from sensor_type").all()
        metrics = [x["name"] for x in results]
        self.assertCountEqual(valid_metrics, metrics)

        print("\t Asserting that metric types are only temperature,rainFall and pH")

        self.assertListEqual(sorted(metrics), sorted(valid_metrics))


if __name__ == '__main__':
    print('Started running Database tests')
    unittest.main()
