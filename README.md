# SolitaFarms
The project uses python programming language

## Setting up the project
All dependencies of the project has been exported to the **environment.yml** file.

Install anaconda or miniconda a create the virtual environment with the command below
````bash 
    conda env create -f environment.yml 

## The database
The databases uses SQLite, hence no installation is need. 

### setting up the database
* Ensure that you have setup the virtual environment as described above
* open the command prompt at the root of the project folder
* run the command 
    ````bash 
        python -m setupdb
