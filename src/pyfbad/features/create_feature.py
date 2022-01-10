import logging
import pandas as pd
from datetime import datetime, timedelta


class Features:

    def get_model_data(self, df, time_column_name, value_column_name, filter=None):
        """ Returns a two column dataframe ready to use train model.
        Args:
            df (Dataframe): A data frame contains a bunch of column
            time_column_name (str): The column name will be defined time axis
            value_column_name (str): The column name will be used as main data to train
            filter (list): To takes only this "value" from the "column_name" --> ['country','TR'] 
        Returns:
            df_ (Dataframe): Two column dataframe ready to use train model
        """
        print("Preparing expected column names and getting model data...")
        try:
            columns = [time_column_name, value_column_name]
            df_ = df[df[filter[0]] == filter[1]].reset_index(drop=True) if filter != None else df

            return df_[columns] \
                .rename(columns={time_column_name: 'ds', value_column_name: 'y'}) \
                .sort_values('ds', ascending=True) \
                .reset_index(drop=True)
        except:
            print("Something went wrong when get the dataframe as ready to train.")