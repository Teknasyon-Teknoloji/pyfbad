from fbprophet import Prophet
from sqlalchemy import *

import json
import logging
import pandas as pd
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

class Model_IsolationForest:

    def train_model(self, df_model, date_type=''):
        """ Train a Isolation Forest model with given dataframe.
        Args:
            df_model (Dataframe): Two column dataframe ready to use train model 
        Returns:
            df_model (Dataframe): The results of the training
        """
        df_model['ds'] = pd.to_datetime(df_model['ds'])

        # set timestamp to index
        df_model.set_index('ds', drop=True, inplace=True)
        # resample timeseries to hourly
        if(date_type=="H"):
            df_model = df_model.resample('H').sum()
            df_model['hour'] = [i.hour for i in df_model.index]

        else:
            df_model = df_model.resample('D').sum()
        # creature features from date
        df_model['day'] = [i.day for i in df_model.index]
        df_model['day_of_year'] = [i.dayofyear for i in df_model.index]
        df_model['week_of_year'] = [i.weekofyear for i in df_model.index]
        # df_model['hour'] = [i.hour for i in df_model.index]
        df_model['is_weekday'] = [i.isoweekday() for i in df_model.index]

        model = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.2), random_state=41)

        model.fit(df_model[['y', 'day_of_year', 'week_of_year', 'is_weekday']])

        df_model['scores'] = model.decision_function(df_model[['y', 'day_of_year', 'week_of_year', 'is_weekday']])

        df_model['anomaly_score'] = model.predict(df_model[['y', 'day_of_year', 'week_of_year', 'is_weekday']])

        return df_model


class Model_Prophet:

    def train_model(self, df_model):
        """ Train a Prophet model with given dataframe.
        Args:
            df_model (Dataframe): Two column dataframe ready to use train model 
        Returns:
            forecast (Dataframe): The results of the training
        """
        try:
            # define the model
            m = Prophet()
            # fit the model
            m = m.fit(df_model)
            # use the model to find an outlier
            forecast = m.predict(df_model)
            forecast['actual'] = df_model['y'].reset_index(drop=True)

            return forecast
        except:
            print("Something went wrong when the prophet model training.")

    def train_forecast(self, forecast):
        """ Tries to predict anomalies based on training results.
        Args:
            forecast (Dataframe): The results of the training
        Returns:
            forecasted (Dataframe): The results of the anomaly predidiction.
        """
        try:
            forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'actual']].copy()

            forecasted['anomaly'] = 0
            forecasted.loc[forecasted['actual'] > forecasted['yhat_upper'], 'anomaly'] = 1
            forecasted.loc[forecasted['actual'] < forecasted['yhat_lower'], 'anomaly'] = -1

            forecasted['high_anomaly'] = (forecasted['actual'] - forecasted['yhat_upper']) / forecast['actual']
            forecasted['low_anomaly'] = (forecasted['yhat_lower'] - forecasted['actual']) / forecast['actual']
            forecasted['importance'] = forecasted.apply(
                lambda row: row['high_anomaly'] if row['anomaly'] == 1 else (row['high_anomaly'] + row['low_anomaly']) / 2,
                axis=1)
            forecasted['importance'] = forecasted.apply(
                lambda row: row['low_anomaly'] if row['anomaly'] == -1 else row['importance'], axis=1)

            return forecasted
        except:
            print("Something went wrong when the predict anomalies.")
        