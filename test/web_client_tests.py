import unittest
import flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROME_DRIVER_URL="chromedriver_linux64/chromedriver"
WEB_APP_URL="http://localhost:5000/web/"
HEADLESS_BROWSER=True   

FARMS=[ "Noora's farm",
        "Friman Metsola collective",
        "Organic Ossi's Impact That Lasts plantase",
        "PartialTech Research Farm"
        ]
METRICS=["pH","rainFall","temperature"]

class WebClientTestCase(unittest.TestCase):
    '''
    Test cases for the Web Client 
    '''

    @classmethod
    def setUpClass(cls):
        print ("Testing {}".format( cls.__name__))

    @classmethod
    def tearDownClass(cls):
        print ("Testing ENDED for {}".format( cls.__name__))
        

    def setUp(self):
        '''
        Setup chrome driver, and browser
        '''

        options=webdriver.ChromeOptions()
        if (HEADLESS_BROWSER):
            options.add_argument('headless')
    
        self.driver=webdriver.Chrome(CHROME_DRIVER_URL,options=options)

    def tearDown(self):
        '''
        Close the chrome driver and browser
        '''
        self.driver.close()
        self.driver.quit()

    def test_dropdown_loaded(self):
        '''
        Check that drop down filters are loaded
        '''
        print ('\n(' + self.test_dropdown_loaded.__name__ + ')', \
            self.test_dropdown_loaded.__doc__)

        self.driver.get(WEB_APP_URL)
        print("\t Asserting that Farm List is loaded")
        farmList=WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="farmList"]/option[1]'))
        )
        self.assertIsNotNone(farmList)
        
        print("\t Asserting that the Farm List has a farm which is either of these: {}".format(FARMS))
        self.assertIn(farmList.text, FARMS)

    def test_data_table_loaded(self):
        '''
        Check that data table is loaded
        '''
        print ('\n(' + self.test_data_table_loaded.__name__ + ')', \
            self.test_data_table_loaded.__doc__)

        self.driver.get(WEB_APP_URL)
        print("\t Asserting that Data Table is loaded")
        dataTable=WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="dataTable"]/tbody/tr[1]/td[1]'))
        )
        self.assertIsNotNone(dataTable)

        print("\t Asserting that the Data Table loads data")
        self.assertNotEqual(dataTable.text, "")

        print("\t Asserting that the Data Table has a farm which is either of these: {}".format(FARMS))
        self.assertIn(dataTable.text, FARMS)
        
    def test_plots_loaded(self):
        '''
        Check that plots are loaded
        '''
        print ('\n(' + self.test_plots_loaded.__name__ + ')', \
            self.test_plots_loaded.__doc__)

        self.driver.get(WEB_APP_URL)
        print("\t Asserting that Average plot is loaded")
        averagePlot=WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="chartAverageContainer"]/div/canvas[1]'))
        )
        self.assertIsNotNone(averagePlot)

        print("\t Asserting that Count plot is loaded")
        countPlot = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="chartCountContainer"]/div/canvas[1]'))
             )
        self.assertIsNotNone(countPlot)

if __name__ == '__main__':
    print ('Started running REST API tests')
    unittest.main()