'''
Creates and populates SolitaFarms databse

@author: asare

'''

from src import database

DB_PATH="data/db/solitafarms.db"
dbEngine=database.Engine(DB_PATH)

print ('\tRemoving old database if any ...')
dbEngine.remove_database()

print('\tCreating database ...')
dbEngine.create_tables()

print('\tPopulating database ....')
dbEngine.populate_tables()

