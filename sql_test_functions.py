# Use pandas to convert csv to db
import pandas as pd
from sql import SQLConnection
#TODO find classes for these functions

# dbName = 'global_sea_levels_nosignals'
# Converts a csv to a db file and prints the db as an output
def csv_to_db(db_name):
  
  # Create db object
  db = open(f'data/{db_name}.db', 'w')
  # Close file
  db.close()

  # Connect to created database
  conn = SQLConnection(f'data/{db_name}.db')

  # Get data from CSV using pandas
  sea_level_data = pd.read_csv(f'data/{db_name}.csv')

  # if_exists can be 'replace', 'append' or 'error' and defines behaviour when chosen table name already exists
  # conn defines the db this table is being added to
  sea_level_data.to_sql(db_name, conn, if_exists = 'replace', index = False)

  # Define a queue
  q = f'SELECT * FROM {db_name}'

  # Iterate through connection printing each row
  for r in conn.queue(q):
    print(r)


