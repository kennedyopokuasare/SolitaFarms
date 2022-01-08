import os
import sys
import json
from datetime import datetime
from flask import render_template,Flask, request

from src import resources

#app = Flask(__name__)
app=resources.app

@app.route('/web')
@app.route('/web/home')
def index():
    '''
    Renders the home page
    '''
    return render_template(
        'solita_farms.html',
        title="Solita Farms",
        year=datetime.now().year
    )

#Start the application
if __name__ == "__main__":
    #Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)