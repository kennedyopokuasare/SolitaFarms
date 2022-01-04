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
The databases uses **SQLite**, hence no installation is needed.

### Setting up the database
* Ensure that you have setup the virtual environment as described above
* run the following command at the root of the project folder
    ````bash 
        python -m setupdb
    ````

At this point, the database is created at `data/db/solitafarms.db` and populated will all the csv data at the `data/external` directory.  If the database already exists, it is deleted and recreated.

A SQL dump of the database schema and data can be found at `data/db/solitafarms.db.sql`