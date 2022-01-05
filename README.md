# SolitaFarms
The project uses python programming language

## Setting up the project
This project uses a python virtual environment to setup all the dependencies.

To begin the setup of the virtual environment
*  Install python (version 3.9)
*  Install anaconda or [miniconda](https://docs.conda.io/en/latest/miniconda.html)

All dependencies of the project has been exported to a virtual environment configuration file **environment.yml**.

Create and activate the virtual environment with the command below

````bash 
    conda env create -f environment.yml
    conda activate solita 
````
if the virtual environment is setup and activated correcly the prompt should show
   `(solita)` 

## The database
The database uses **SQLite**, hence no installation is needed. 
The database also uses **SQLAlchemy** library for database access and object relational mapping

### Setting up the database
* Ensure that you have setup the virtual environment as described above
* run the following command at the root of the project folder
    ````bash 
        python -m setupdb
    ````

At this point, the database is created at `data/db/solitafarms.db` and populated will all the csv data at the `data/external` directory.  If the database already exists, it is deleted and recreated.

A SQL dump of the database schema and data can be found at `data/db/solitafarms.db.sql`

## The REST API
The REST API was implemented using **FLASK microframework**(http://flask.pocoo.org/) which is a python framework.  


## Setting up and running the API
To setup and run the API, please follow the following steps

1. Ensure the project and database is setup as described in the **Setting up the project** and **The database** sections
2. run the command at the root of the project folder
    ````bash
        python -m src.resources
    ````
3. The command in step 2  will start the FLASK built in web server with the address **http://localhost:5000** , or a similar address. The actual address will be displayed in the command prompt. 
4. The endpoints of the api are as follow:
    * List all farms */solitafarms/farms/*
    * 
5. You can also use any rest client to test the API    
### Running test