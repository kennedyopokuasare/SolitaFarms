from src.entities import SensorData, SensorType, Farm
class FarmsDao(object):

    def __init__(self,db_Session):
        super(FarmsDao,self).__init__()
        if db_Session is None:
            raise Exception("Database session cannot be None")
        self.db_session=db_Session

    def get_all_farms(self):
        return self.db_session.query(Farm).all()

        