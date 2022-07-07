import pandas as pd


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
            df_ = df[df[filter[0]] == filter[1]].reset_index(
                drop=True) if filter != None else df

            return df_[columns] \
                .rename(columns={time_column_name: 'ds', value_column_name: 'y'}) \
                .sort_values('ds', ascending=True) \
                .reset_index(drop=True)
        except Exception:
            raise Exception(
                "Error when cleaning dataframe to extract features...")

    def extract_features(self, df_model, date_type, model_name):
        """ Create extra features from date value in dataframe.
        Args:
            df_model (Dataframe): dataframe ready to use train model 
            date_type (str): data time range type, daily or hourly   
            model_name (str): name of the model, IF or GMM  
        Returns:
            df_model (Dataframe): feature extacted dataframe
        """
        try:
            df_model['ds'] = pd.to_datetime(df_model['ds'])

            # set timestamp to index
            df_model.set_index('ds', drop=True, inplace=True)

            if date_type == "H":
                df_model = df_model.resample('H').sum()
                df_model['hour'] = [i.hour for i in df_model.index]
            else:
                df_model = df_model.resample('D').sum()

            # create features from date
            df_model['day'] = [i.day for i in df_model.index]
            df_model['month'] = [i.month for i in df_model.index]
            df_model['year'] = [i.year for i in df_model.index]
            df_model['week_of_year'] = [i.weekofyear for i in df_model.index]
            df_model['weekday'] = [i.isoweekday() for i in df_model.index]

            if model_name == "IF":
                df_model['day_of_year'] = [i.dayofyear for i in df_model.index]
            elif model_name == "GMM":
                df_model['quarter'] = [i.quarter for i in df_model.index]
                df_model["is_weekday"] = df_model['weekday'].apply(
                    lambda x: 0 if (x == 6) | (x == 7) else 1)
            return df_model
        except Exception:
            raise Exception("Error when extracting feature from dataframe...")
