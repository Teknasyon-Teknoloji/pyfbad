import pandas as pd


class Features:

    def transform_data(self, df, time_column_name, value_column_name, filter=None):
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
            df_ = df[df[filter[0]] == filter[1]].reset_index(
                drop=True) if filter != None else df
            return df_[columns] \
                .rename(columns={time_column_name: 'ds', value_column_name: 'y'}) \
                .sort_values('ds', ascending=True)
        except Exception:
            raise Exception(
                "Error when cleaning dataframe to extract features...")

    def extract_time_features(self, df_):
        """ Create extra features from date value in dataframe.
        Args:
            df_ (Dataframe): A dataframe contains a bunch of column
        Returns:
            df_ (Dataframe): A dataframe that contains extra time features
        """
        try:
            # create features from date
            df_['day'] = [i.day for i in df_.index]
            df_['month'] = [i.month for i in df_.index]
            df_['quarter'] = [i.quarter for i in df_.index]
            df_['year'] = [i.year for i in df_.index]
            df_['day_of_year'] = [i.dayofyear for i in df_.index]
            df_['week_of_year'] = [i.weekofyear for i in df_.index]
            df_['weekday'] = [i.isoweekday() for i in df_.index]
            df_["is_weekday"] = df_['weekday'].apply(
                lambda x: 0 if (x == 6) | (x == 7) else 1)
            return df_
        except Exception:
            raise Exception("Error when extracting feature from dataframe...")

    def get_modeling_data(self, df_model, model_name, date_type="D"):
        """ Returns a dataframe with extracted time features for modeling.
        Args:
            df_model (Dataframe): dataframe ready to use train model    
            model_name (str): name of the model, IF or GMM  
            date_type (str): data time range type, daily or hourly
        Returns:
            df_model (Dataframe): feature extacted dataframe
        """
        try:
            # set timestamp to index
            df_model.set_index('ds', inplace=True)

            if date_type == "H":
                df_model = df_model.resample('H').sum()
                df_model['hour'] = [i.hour for i in df_model.index]
            else:
                df_model = df_model.resample('D').sum()

            df_model = self.extract_time_features(df_model)

            if model_name in ["IF", "LOF"]:
                return df_model.drop(['quarter', 'is_weekday'], axis=1)
            elif model_name == "GMM":
                return df_model.drop(['day_of_year'], axis=1)
            elif model_name == "Prophet":
                return df_model.reset_index()[["ds", "y"]]
            else:
                return df_model
        except Exception:
            raise Exception(
                "Error when getting dataframe ready for modeling...")
