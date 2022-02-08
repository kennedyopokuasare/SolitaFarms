import unittest
import json
import flask

from src import database
from src import resources

DB_PATH = 'data/db/solitafarms_test.db'
dbEngine = database.Engine(DB_PATH)

JSON = "application/json"
FARM_LIST = "/solitafarms/farms/"
WRONG_URL = "/solitafarms/farms-wrong/"
# wrong month: No month 23 in a Year
WRONG_URL_VARIABLES_VALUES = "/solitafarms/farms/1/month/23/"

resources.app.config.update({"Engine": dbEngine})
resources.app.config["TESTING"] = True


class RestAPITestCase(unittest.TestCase):
    '''
    Test cases for the REST API 
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
        Populates the database and sets up flask test client
        '''
        dbEngine.populate_tables()

        self.client = resources.app.test_client()

    def tearDown(self):
        '''
        Remove all records from database.
        '''
        dbEngine.clear_records()

    def test_wrong_url(self):
        '''
        Check that wrong url returns 404 status code
        '''
        print('\n(' + self.test_wrong_url.__name__ + ')',
              self.test_wrong_url.__doc__)

        response = self.client.get(WRONG_URL)
        print("\tAsserting that wrong url returns 404 status code")
        self.assertEqual(response.status_code, 404)

    def test_invalid_url_variable_value(self):
        '''
        Check that url variable values are validated
        '''
        print('\n(' + self.test_invalid_url_variable_value.__name__ + ')',
              self.test_invalid_url_variable_value.__doc__)

        response = self.client.get(WRONG_URL_VARIABLES_VALUES)
        print("\tAsserting that invalid url variable value returns 403 status code")
        self.assertEqual(response.status_code, 403)

        resp_data = json.loads(response.data)
        print("\tAsserting that response has message JSON key")
        message = resp_data["message"]
        self.assertIsNotNone(message)
        print("\tAsserting that response has message JSON value is not empty")
        self.assertNotEqual(message, "")

    def test_get_farms_list(self):
        '''
        Check that GET farms list returns correct status code and data format 
        '''
        print('\n(' + self.test_get_farms_list.__name__ + ')',
              self.test_get_farms_list.__doc__)

        response = self.client.get(FARM_LIST)
        print("\tAsserting that response has status code 200")
        self.assertEqual(response.status_code, 200)

        print("\tAsserting that response headers have application/json content type")
        self.assertEqual(response.headers.get("Content-Type"), JSON)

        print("\tAsserting that response is in JSON format")
        resp_data = json.loads(response.data)
        self.assertIsNotNone(resp_data)

        print("\tAsserting that response has data JSON object")
        data = resp_data["data"]
        self.assertIsNotNone(data)

        print("\tAsserting that reponse data JSON object contains rows")
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    print('Started running REST API tests')
    unittest.main()
