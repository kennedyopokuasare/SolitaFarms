import json

from flask import Flask, request,jsonify, Response, g, _request_ctx_stack, redirect
from werkzeug.exceptions import HTTPException, NotFound

from src import database
from src import databaseDao as dao

app = Flask(__name__)
app.debug = True

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
    

    return Response(json.dumps(envelope), status_code, mimetype="application/json")


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

    if hasattr(g, "con"):
        g.session.close()

@app.route("/",methods=["GET"])
def home():
   return redirect("/solitafarms/")

@app.route("/solitafarms/",methods=["GET"])
def api_home():
    endpoints={
        "all_farms":"/solitafarms/farms/"
    }
    return create_response("201",data=endpoints, message="Welcome to the API home.")

@app.route("/solitafarms/farms/",methods=["GET"])
def get_farm_list():
    all_farms=dao.FarmsDao(g.session).get_all_farms()
    return create_response(200,data=all_farms)

#Start the application
#DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == "__main__":
    #Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)

