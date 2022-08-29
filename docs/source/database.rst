Database
=======

pyfbad.data.database.MongoDB
------------------------

  >>> __init__(self, db_name, db_port, db_path)
To initialize the mongodb connection.

  >>> get_mongo_db(self)
Builds client and database objects to be read from.

  >>> get_collection_names(self, database)
Returns the collection names from given database.

  >>> get_data(self, database, collection, filter=None)
Reads data from database given a collection name. 
If necessary, filter option takes a list of dictionary. 
add_filter method should be used to build.

  >>> get_data_as_df(self, database, collection, filter=None)
Reads data from database given a collection name.

If necessary, filter option takes a list of dictionary. 

add_filter method should be used to build.

  >>> add_filter(self, filter_array, type, value)
Add filter to mongodb query in time, value, group and sort domains.

  >>> writing_to_db(self, database, transformed, collection)
Writing detected anomalies to mongodb collections.


pyfbad.data.database.SQLDB
---------------------

  >>> __init__(self, **kwargs)
Get the connection configuration for database with kwargs.

  >>> set_db_conn(self)
Set a connection configuration for database.

  >>> create_db_conn(self)
Create database engine to connect database.

  >>> reading_rawdata(self, query, db_conn, table_name)
Reading row data from db with sql query.

  >>> writing_to_db(self, data, db_conn, table_name, chunksize=10000, if_exists="append")
Writing detected anomalies to database table.

**db_conn (Database instance):** Engine instance

**table_name (str):** database table name for dataframe

**chunksize (integer):** number of rows in each batch to be written.

**if_exists (str):** appending new values to existing db table

pyfbad.data.database.CloudDB
------------------------

  >>> __init__(self, key_path, project_name)
Get the connection configuration for GCP BigQuery.

**key_path (str):** Service account JSON file path

**project_name (str):** Contains BigQuery project name

  >>> reading_raw_data(self, query_string)
Reading raw data from BigQuery.

  >>> writing_to_bq(self, dataframe, dataset, table_name)
It writes dataframe to bq, If table is exist it adds inside of it, else it creates table first.

pyfbad.data.database.File
---------------------

  >>> read_from_csv(self, time_column_name, file_path, filter=None)
Reads data from csv file.

**time_column_name (str):** name of the time column in dataset

**file_path (str):** file path of csv file

**filter (array):** column_name,value

  >>> writing_to_csv(self, data, file_path, index=False)
Writes data to csv file.

**data (DataFrame):** dataframe that will be written to csv

**file_path (str):** csv file path of dataframe to write

**index (boolean):** booelan value of whether add or not index to csv
