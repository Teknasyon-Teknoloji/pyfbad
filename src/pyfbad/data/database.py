from typing import Collection
from sqlalchemy import *
import pandas as pd
import sys
from datetime import datetime, timedelta
import pymongo
from sshtunnel import SSHTunnelForwarder


class MongoDB:
    def __init__(self, db_name, db_port, db_path): 
        """ To initialize the mongodb connection.
        Args:
            db_name (str): Database name ex. myMongoDB
            db_port (int): Port name ex. 27017
            db_path (str): Database path ex. 127.0.0.1
        """
        self._db_name = db_name
        self._db_port = db_port
        self._db_path = db_path
        
    def get_mongo_db(self):
        """ Builds client and database objects to be read from.
        Returns:
            database (MongoClient): Database client object to read from
        """
        _config = {
            'db_name' : self._db_name,
            'db_path' : self._db_path,
            'db_port' : self._db_port,
        }
        try:
            print("mongo init...")
            client = pymongo.MongoClient(_config['db_path'],_config['db_port'])
            database = client[_config['db_name']]
            print("mongo init done")

            return database
        except:
            print("Something went wrong when build the MongoDB client.")
        
    def get_collection_names(self, database):
        """ Returns the collection names from given database.
        Args:
            database (MongoClient): Database client object to read from
        Returns:
            collections (list): Name of the collections in database
        """
        print("List of the collections:")
        try:
            collections = database.list_collection_names()
        except:
            print("Something went wrong when get the list of collection names.")

        return collections

    def get_data_from_one_collection(self, database, collection, filter=None):
        """ DEPRECATED!!!
        Reads data from database given a collection name.
        If necessary, filter option takes a range of dates given
        in ['name_of_time_column','starting_date','finishing_date'] format.
        Args:
            collection (str): name of the collection in database
            database (MongoClient): Database client object to read from
            filter (list(float)): 
                Value filter: column name, value
                Time filter: column name, Start and end point of the time
        Returns:
            records (mongodb obj): A cursor(pointer) to the selected documents
        """
        collection = database[collection]
        if filter is None:
            records = collection.find()
        elif 'time' and 'value' in filter:
            records = collection.find(
                {filter['time']['column_name']:{'$gte': filter['time']['start_time'], '$lte': filter['time']['finish_time']}},
                {filter['value']['column_name']: filter['value']['value']}
                )
        elif 'time' in filter:
            records = collection.find(
                {filter['time']['column_name']:{'$gte': filter['time']['start_time'], '$lte': filter['time']['finish_time']}}
                )
        elif 'value' in filter:
            records = collection.find(
                {filter['value']['column_name']: filter['value']['value']}
                )
        return records

    def get_data(self, database, collection, filter=None):
        """ Reads data from database given a collection name.
        If necessary, filter option takes a list of dictionary. add_filter method
        should be used to build.
        Args:
            collection (str): name of the collection in database
            database (MongoClient): Database client object to read from
            filter (list(dict)): Should be build with add_filet method first
        Returns:
            records (mongodb obj): A cursor(pointer) to the selected documents
        """
        try:
            collection = database[collection]
            if filter is None:
                records = collection.find()
            else:
                records = collection.aggregate(filter)

            return records
        except:
            print("Something went wrong when get the data from the collection.")
    
    def get_data_as_df(self, database, collection, filter=None):
        """ Reads data from database given a collection name.
        If necessary, filter option takes a list of dictionary. add_filter method
        should be used to build.
        Args:
            collection (str): name of the collection in database
            database (MongoClient): Database client object to read from
            filter (list(dict)): Should be build with add_filet method first
        Returns:
            records (df): A dataframe to the selected documents
        """
        try:
            collection = database[collection]
            if filter is None:
                data = collection.find()
            else:
                data = collection.aggregate(filter)

            records = pd.json_normalize(list(data))

            return records
        except:
            print("Something went wrong when get the dataframe from the collection.")

    def add_filter(self, filter_array, type, value):
        """ Add filter to mongodb query in time, value, group and sort domains.
        Args:
            filter_array (list): An array that contains the filter dictionaries.
            type (str): Filter type ex. time, value, group or sort.
            value (dict): Should be consist with the type of the filter. Ex.
                add_filter(
                    [],
                    'time',
                    {
                        "column_name": "date",
                        "date_type": "hourly",
                        "start_time": "2019-02-06 00:00:00",
                        "finish_time": "2019-03-06 00:00:00"
                    }
                )
        Returns:
            filter_array (list(dict)): A list of dictionaries that contains the filter .
        """
        if type == 'time':
            if value["date_type"] == 'hourly':
                date_format = '%Y-%m-%d %T'
                filter = {
                    "$match": {value['column_name']:{'$gte': value['start_time'], '$lte': value['finish_time']}}
                }
                filter_array.append(filter)
            elif value["date_type"] == 'daily':
                date_format = '%Y-%m-%d 00:00:00'
                filter = {
                    "$match": {value['column_name']:{'$gte': value['start_time'], '$lte': value['finish_time']}}
                }
                filter_array.append(filter)
        elif type == 'value':
            filter = {
                "$match": {value['column_name']: value['value']}
            }
            filter_array.append(filter)
        elif type == 'group':
            id = {"_id": {}}
            for i in value:
                if 'column_name' in i:
                    id["_id"][i['column_name']] = str('$' + i['column_name'])
                elif 'count' in i:
                    id["count"] = {str('$' + i['count']) :i['desc']}
            filter = {
                    "$group": id
                }
            filter_array.append(filter)
        elif type == 'sort':
            filter = {
                "$sort": {value['column_name'] : value['desc']}
            }
            filter_array.append(filter)
        else:
            print("Something went wrong when build the mongodb query. Please check your input variables.")
        return filter_array

class MySQLDB:

    def __init__(self):
        print("in init")

    def get_mysql_db(self, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE):
        """ Set the initial configuration for mysql.
        Args:
            MYSQL_USERNAME (str): Database username.
            MYSQL_PASSWORD (str): Databse password
            MYSQL_HOST (str): Database host name
            MYSQL_PORT (str): Database port name
            MYSQL_DATABASE (str): Database name
        """
        _config = {
            'MYSQL_USERNAME': MYSQL_USERNAME,
            'MYSQL_PASSWORD': MYSQL_PASSWORD,
            'MYSQL_HOST': MYSQL_HOST,
            'MYSQL_PORT': MYSQL_PORT,
            'MYSQL_DATABASE': MYSQL_DATABASE
        }

        try:
            print("MySQL init...")

            self.mysql_connection_string = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
                _config['MYSQL_USERNAME'],
                _config['MYSQL_PASSWORD'],
                _config['MYSQL_HOST'],
                _config['MYSQL_PORT'],
                _config['MYSQL_DATABASE'])

            # self.mysql_schema = _config['MYSQL_DATABASE']
            print("MySQL init done.")
        except:
            print("Something went wrong when configure the initial setup. Please check your input variables.")
        
    def create_mysql_conn(self):
        """ Create database engine to connect mysql database
        Returns:
            engine (Database instance): Engine instance
        """
        try:
            engine = create_engine(self.mysql_connection_string)
            return engine.connect()
        except:
            print("Something went wrong when creating the database engine.")

    def getting_raw_data_query_from_mysql(self, query, conn_mysql):
        """ Reads data from database with mysql query.
        Args:
            query (str): Mysql query
            conn_mysql (engine instance): Mysql engine instance
        Returns:
            (Dataframe): A dataframe queried with given parameters.
        """
        try:
            print("Getting raw data from MySQL...")
            return pd.read_sql_query(text(query), conn_mysql)
        except Exception as e:
            print(e.args)
            sys.exit(1)

class File:
    def __init__(self) -> None:
        pass

    def read_from_csv(self, file_path, filter=None):
        """
        :param file_path: string
        :param filter: array [column_name,value]
        :return: dataframe
        """
        df = pd.read_csv(file_path)
        df_ = df[df[filter[0]] == filter[1]].reset_index(drop=True) if filter != None else df
        
        return df_