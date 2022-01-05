import json

from flask import Flask, request,jsonify, Response, g, _request_ctx_stack, redirect
from werkzeug.exceptions import HTTPException, NotFound

from src import database
from src import databaseDao as dao

from src.utils import CustomJSONEncoder

app = Flask(__name__)
app.debug = True
app.json_encoder=CustomJSONEncoder

app.config.update({"Engine": database.Engine()})


def create_response(status_code,data=None,message=None):
    """
    Creates a response of an API call. 

    :param status_code: the response status code
    :param data: response data
    :param message: response message
    """
    envelope=dict()
    if message is not None:
        envelope["message"]=message
    if data is not None:
        envelope["data"]=data
    
    response=jsonify(envelope)
    response.status_code=status_code
    return response


@app.errorhandler(404)
def resource_not_found(error):
    return create_response(404,message= "Resource not found. This resource url does not exit")
@app.errorhandler(500)
def unknown_error(error):
    return create_response(500,message= "Error.  Please, contact the administrator")

@app.before_request
def connect_db():
    """
    Creates a database session before the request is proccessed.
    The session is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    """
    g.session=app.config["Engine"].get_dbSession()


@app.teardown_request
def close_connection(exc):
    """ 
    Closes the database session
    Check if the session is created. 
    """

    if hasattr(g, "session"):
        g.session.close()

@app.route("/",methods=["GET"])
def home():
   return redirect("/solitafarms/")

@app.route("/solitafarms/",methods=["GET"])
def api_home():

    return create_response("201",message="Welcome to the Solita Farms API.")

@app.route("/solitafarms/farms/",methods=["GET"])
def get_farm_list():
    with g.session as session:
        all_farms=dao.FarmsDao(session).get_all_farms()
        #output validation
        if (all_farms is None) or (len(all_farms)==0) :
            return create_response(200,data=[],message="No farms exists!")
        return create_response(200,data=all_farms)

@app.route("/solitafarms/metrics/",methods=["GET"])
def get_metric_list():
    with g.session as session:
        all_metrics=dao.FarmsDao(session).get_all_metrics()
        #output validation
        if (all_metrics is None) or (len(all_metrics)==0) :
            return create_response(200,data=[],message="No metrics exists!")
        return create_response(200,data=all_metrics)
@app.route("/solitafarms/farms/<int:farmId>/month/<int:monthOfYear>/",methods=["GET"])
def get_farm_data_by_month(farmId:int,monthOfYear:int):
    #input validation 
    #First level of input validation done url formating. The url variables should be an int and and int
    #other the resource will not be found.
    # Checking the monthOfYear range as another level of input validation
    if monthOfYear <1 or monthOfYear>12:
        return create_response(403,message="Invalid url variables. monthOfYear should be from 1 to 12")

    with g.session as session:
        try:
          results=dao.FarmsDao(session).get_farm_data_by_month(farmId, monthOfYear)
          print(results)
          return create_response(200,results)
        except Exception as eror:
           
            return create_response(403,message="{}".format(eror))



    return create_response(200)

@app.route("/solitafarms/farms/<int:farmId>/metric/<int:metricId>/",methods=["GET"])
def get_farm_data_by_metric(farmId,metricId):
    pass

#Start the application
#DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == "__main__":
    #Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)

