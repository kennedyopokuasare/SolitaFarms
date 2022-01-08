from src.entities import SensorData, SensorType, Farm
from sqlalchemy import extract, func

class FarmsDao(object):

    def __init__(self,db_Session):
        super(FarmsDao,self).__init__()
        if db_Session is None:
            raise Exception("Database session cannot be None")
        self.db_session=db_Session

    def get_farm(self,farmId):
        return self.db_session.query(Farm).filter(Farm.id==farmId).first()

    def get_all_farms(self):
        return self.db_session.query(Farm).all()

    def get_metric(self,metricId):
        return self.db_session.query(SensorType).filter(SensorType.id==metricId).first()

    def get_all_metrics(self):
        return self.db_session.query(SensorType).all()

    def get_farm_data(self,farmId:int):
        data=dict()
        farm=self.get_farm(farmId)
        if farm is None:
           raise Exception("No such Farm exist with id {}".format(farmId))

        data["farm"]=farm
        results=self.db_session.query(
                                        SensorData.id,
                                        SensorData.date,
                                        SensorType.name.label("metric"),
                                        SensorData.value    
                                        ) \
                    .join(SensorType)\
                    .filter(SensorData.farm_id==farmId)\
                    .all()

        farmData=[]
        if (results is not None) and (len(results)>0 ):
            keys=["id","date","metric","value"]
            farmData=[{key:row[key] for key in keys} for row in results]
        
        data["sensor_data"]=farmData
        
        return data

    def get_farm_data_by_month(self,farmId:int,monthOfYear:int):
        data=dict()
        farm=self.get_farm(farmId)
        if farm is None:
           raise Exception("No such Farm exist with id {}".format(farmId))

        data["farm"]=farm
        results=self.db_session.query(
                                        SensorData.id,
                                        SensorData.date,
                                        SensorType.name.label("metric"),
                                        SensorData.value    
                                        ) \
                    .join(SensorType)\
                    .filter(SensorData.farm_id==farmId)\
                    .filter(extract('month',SensorData.date)==monthOfYear)\
                    .all()
                    
        farmData=[]
        if (results is not None) and (len(results)>0 ):
            keys=["id","date","metric","value"]
            farmData=[{key:row[key] for key in keys} for row in results]
        
        data["sensor_data"]=farmData
        
        return data
    
    def get_farm_data_by_metric(self,farmId:int,metricId:int):
        data=dict()
        farm=self.get_farm(farmId)
        if farm is None:
           raise Exception("No such Farm exist with id {}".format(farmId))

        metric=self.get_metric(metricId)
        if metric is None:
            raise Exception("No such Metric exists with id {}".format(metricId))

        data["farm"]=farm
        results=self.db_session.query(
                                        SensorData.id,
                                        SensorData.date,
                                        SensorType.name.label("metric"),
                                        SensorData.value    
                                        ) \
                    .join(SensorType)\
                    .filter(SensorData.farm_id==farmId)\
                    .filter(SensorData.sensor_type_id==metricId)\
                    .all()
        farmData=[]
        if (results is not None) and (len(results)>0 ):
            keys=["id","date","metric","value"]
            farmData=[{key:row[key] for key in keys} for row in results]
        
        data["sensor_data"]=farmData
        
        return data
    
    def get_farm_monthtly_metric_aggregates(self,farmId:int,metricId:int):
        data=dict()
        farm=self.get_farm(farmId)
        if farm is None:
           raise Exception("No such Farm exist with id {}".format(farmId))

        metric=self.get_metric(metricId)
        if metric is None:
            raise Exception("No such Metric exists with id {}".format(metricId))

        data["farm"]=farm
        results=self.db_session.query(
                                        SensorType.name.label("metric"),
                                        extract('month',SensorData.date).label("month"),
                                        extract('year',SensorData.date).label("year"),
                                        func.count(SensorData.value).label("count"),
                                        func.max(SensorData.value).label("max"),
                                        func.min(SensorData.value).label("min"),
                                        func.avg(SensorData.value).label("average"),
                                        func.sum(SensorData.value).label("sum"),
                                        ) \
                    .join(SensorType)\
                    .filter(SensorData.farm_id==farmId)\
                    .filter(SensorData.sensor_type_id==metricId)\
                    .group_by(SensorType.name.label("metric"),
                                extract('month',SensorData.date).label("month"),
                                extract('year',SensorData.date).label("year")
                            )\
                    .all()
        farmData=[]
        if (results is not None) and (len(results)>0 ):
            keys=["metric","month","year","count","max","min","average","sum"]
            farmData=[{key:row[key] for key in keys} for row in results]
        
        data["metric_aggregates"]=farmData
        
        return data