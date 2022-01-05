from src.entities import SensorData, SensorType, Farm
from sqlalchemy import extract  
class FarmsDao(object):

    def __init__(self,db_Session):
        super(FarmsDao,self).__init__()
        if db_Session is None:
            raise Exception("Database session cannot be None")
        self.db_session=db_Session

    def get_all_farms(self):
        return self.db_session.query(Farm).all()

    def get_all_metrics(self):
        return self.db_session.query(SensorType).all()

    def get_farm_data_by_month(self,farmId:int,monthOfYear:int):
        data=dict()
        farm=self.db_session.query(Farm).filter(Farm.id==farmId).first()
        if farm is None:
           raise Exception("No such Farm exist with id {}".format(farmId))

        data["farm"]=farm
        farmData=self.db_session.query(SensorData) \
                     .filter(SensorData.farm_id==farmId)\
                     .filter(extract('month',SensorData.date)==monthOfYear)\
                     .all()
        data["sensor_data"]=farmData
        
        return data