from sqlalchemy import *
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pymongo


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
            'db_name': self._db_name,
            'db_path': self._db_path,
            'db_port': self._db_port,
        }
        try:
            print("mongo init...")
            client = pymongo.MongoClient(
                _config['db_path'], _config['db_port'])
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
                {filter['time']['column_name']: {'$gte': filter['time']
                                                 ['start_time'], '$lte': filter['time']['finish_time']}},
                {filter['value']['column_name']: filter['value']['value']}
            )
        elif 'time' in filter:
            records = collection.find(
                {filter['time']['column_name']: {'$gte': filter['time']
                                                 ['start_time'], '$lte': filter['time']['finish_time']}}
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
                    "$match": {value['column_name']: {'$gte': value['start_time'], '$lte': value['finish_time']}}
                }
                filter_array.append(filter)
            elif value["date_type"] == 'daily':
                date_format = '%Y-%m-%d 00:00:00'
                filter = {
                    "$match": {value['column_name']: {'$gte': value['start_time'], '$lte': value['finish_time']}}
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
                    id["count"] = {str('$' + i['count']): i['desc']}
            filter = {
                "$group": id
            }
            filter_array.append(filter)
        elif type == 'sort':
            filter = {
                "$sort": {value['column_name']: value['desc']}
            }
            filter_array.append(filter)
        else:
            print(
                "Something went wrong when build the mongodb query. Please check your input variables.")
        return filter_array

    def writing_to_db(self, database, transformed, collection):
        """ Writing detected anomalies to mongodb collections.
        Args:
            database (database) : mongodb database
            transformed (DataFrame): Contains the data we processed
            collection (str): Name of the destination collection
        Returns: None
        """
        database[collection].insert_many(transformed.to_dict("records"))


class SQLDB:

    def __init__(self, **kwargs):
        """ Get the connection configuration for database with kwargs.
        Args:
        Returns: None
        """
        try:
            self.db = kwargs.get('db')
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.host = kwargs.get('host')
            self.port = kwargs.get('port')
            self.database = kwargs.get('database')
        except Exception:
            raise Exception("Error when getting configurations with kwargs...")

    def set_db_conn(self):
        """ Set a connection configuration for database.
        Args: None
        Returns: None
        """
        try:
            print("Setting up database connection parameters...")
            self.connection_string = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
                self.db,
                self.username,
                self.password,
                self.host,
                self.port,
                self.database)
        except Exception:
            raise Exception("Error when setting db connection parameters...")

    def create_db_conn(self):
        """ Create database engine to connect database.
        Args: None
        Returns:
            engine (Database instance): Engine instance
        """
        try:
            print("Creating database connection...")
            engine = create_engine(self.connection_string)
            return engine.connect()
        except Exception:
            raise Exception("Error when creating database connection...")

    def reading_rawdata(self, query, db_conn, table_name):
        """ Reading row data from db with sql query.
        Args: 
            query (str): Database username
            db_conn (Database instance): Engine instance
            table_name (str): database table name for dataframe
        Returns: data (DataFrame): A dataframe ingested with sql query
        """
        try:
            print("Reading data from {0}...".format(table_name))
            return pd.read_sql_query(query, db_conn)
        except Exception:
            raise Exception("Error when reading rawdata...")
        finally:
            db_conn.close()

    def writing_to_db(self, data, db_conn, table_name, chunksize=10000, if_exists="append"):
        """ Writing detected anomalies to database table.
        Args:
            data (DataFrame): DataFrame that be written to database.
            db_conn (Database instance): Engine instance
            table_name (str): database table name for dataframe
            chunksize (integer): number of rows in each batch to be written.
            if_exists (str): appending new values to existing db table
        Returns: None
        """
        try:
            print("Writing data to {0}...".format(table_name))
            data.to_sql(name=table_name, con=db_conn,
                        chunksize=chunksize, if_exists=if_exists)
        except Exception:
            raise Exception("Error when writing data to table...")
        finally:
            db_conn.close()


class CloudDB:

    def __init__(self, key_path, project_name):
        """Get the connection configuration for GCP BigQuery.
        Args:
            key_path (str): Service account JSON file path
            project_name (str): Contains BigQuery project name
        """
        try:
            self.key_path = key_path
            self.project_name = project_name
            self.credentials = service_account.Credentials.from_service_account_file(
                self.key_path, scopes=[
                    "https://www.googleapis.com/auth/cloud-platform"]
            )
            self.bqclient = bigquery.Client(
                credentials=self.credentials,
                project=self.credentials.project_id,
            )
        except Exception:
            raise Exception(
                "Error when setting GCP BigQuery configurations...")

    def reading_raw_data(self, query_string):
        """ Reading raw data from BigQuery.
        Args:
            query_string (str): It cantains the query
        Returns: Dataframe
        """
        try:
            return self.bqclient.query(query_string).result().to_dataframe()
        except Exception:
            raise Exception(
                "Something went wrong when reading raw data to data frame...")

    def writing_to_bq(self, dataframe, dataset, table_name):
        """It writes dataframe to bq, If table is exist it adds inside of it, else it
            creates table first.
        Args:
            dataframe (DataFrame): Contains the values we want to write to bq
            dataset (str): Contains BigQuery dataset name
            table_name (str): Contains BigQuery table name
        Returns: If result is succeeded empty list will return
        """
        try:
            print("Writing data to {0}...".format(table_name))
            table_id = "{0}.{1}.{2}".format(
                self.project_name, dataset, table_name)
            job = self.bqclient.load_table_from_dataframe(
                dataframe, table_id
            )
            return job.result()
        except Exception:
            raise Exception(
                "Something went wrong when writing  data to BigQuery table...")


class File:

    def __init__(self) -> None:
        pass

    def read_from_csv(self, time_column_name, file_path, filter=None):
        """ Reads data from csv file.
        Args:
            time_column_name (str): name of the time column in dataset
            file_path (str): file path of csv file
            filter (array): column_name,value
        Returns:
            df_ (dataframe): read dataframe
        """
        try:
            df = pd.read_csv(file_path)
            df_ = df[df[filter[0]] == filter[1]].reset_index(
                drop=True) if filter else df
            df_[time_column_name] = pd.to_datetime(df_[time_column_name])
            return df_
        except Exception:
            raise Exception(
                "Something went wrong when reading raw data from csv file...")

    def writing_to_csv(self, data, file_path, index=False):
        """ Writes data to csv file.
        Args:
            data (DataFrame): dataframe that will be written to csv
            file_path (str): csv file path of dataframe to write
            index (boolean): booelan value of whether add or not index to csv
        Returns: None
        """
        try:
            print("Writing data to csv...")
            data.to_csv(file_path, index=index)
        except Exception:
            raise Exception("Error when writing data to csv...")
