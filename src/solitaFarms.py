from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os
from src import resources
from src import views

api = resources.app
webClient = views.app

application = DispatcherMiddleware(api, {
    '/web': webClient
})

if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
