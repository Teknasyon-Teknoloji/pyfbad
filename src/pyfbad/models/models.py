from fbprophet import Prophet
from sqlalchemy import *
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest


class Model_IsolationForest:

    def train_model(self, df_model, date_type='', contamination_value = float(0.2)):
        """ Train a Isolation Forest model with given dataframe.
        Args:
            df_model (Dataframe): Two column dataframe ready to use train model 
            contamination_value (Float): It contains default float value for contamination parameter
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
        # create features from date
        df_model['day'] = [i.day for i in df_model.index]
        df_model['month'] =  [i.month for i in df_model.index]
        df_model['year'] = [i.year for i in df_model.index]
        df_model['day_of_year'] = [i.dayofyear for i in df_model.index]
        df_model['week_of_year'] = [i.weekofyear for i in df_model.index]
        df_model['is_weekday'] = [i.isoweekday() for i in df_model.index]

        model = IsolationForest(n_estimators=100, max_samples='auto', contamination=contamination_value, random_state=41)
        
        if(date_type=="H"):
            model.fit(df_model[['y', 'day','month','year','hour','day_of_year', 'week_of_year', 'is_weekday']])
            df_model['scores'] = model.decision_function(df_model[['y', 'day','month','year','hour','day_of_year', 'week_of_year', 'is_weekday']])
            df_model['anomaly_score'] = model.predict(df_model[['y', 'day','month','year','hour','day_of_year', 'week_of_year', 'is_weekday']])
            return df_model
        
        model.fit(df_model[['y', 'day','month','year','day_of_year', 'week_of_year', 'is_weekday']])
        df_model['scores'] = model.decision_function(df_model[['y', 'day','month','year','day_of_year', 'week_of_year', 'is_weekday']])
        df_model['anomaly_score'] = model.predict(df_model[['y', 'day','month','year','day_of_year', 'week_of_year', 'is_weekday']])
        df_model['anomaly_score'][df_model['anomaly_score'] == 1] = 0
        df_model['anomaly_score'][df_model['anomaly_score'] == -1] = 1
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

    def train_forecast(self, forecast, bound_coefficient):
        """ Tries to predict anomalies based on training results.
        Args:
            forecast (Dataframe): The results of the training
            bound_coefficient (float): optimization coefficient for anomaly number
        Returns:
            forecasted (Dataframe): The results of the anomaly predidiction
        """
        try:
            forecasted = forecast[['ds', 'trend', 'yhat',
                                   'yhat_lower', 'yhat_upper', 'actual']].copy()

            forecasted['anomaly'] = 0
            forecasted['yhat_upper'] = forecasted['yhat_upper'] * \
                bound_coefficient
            forecasted['yhat_lower'] = forecasted['yhat_lower'] / \
                bound_coefficient
            forecasted.loc[forecasted['actual'] >
                           forecasted['yhat_upper'], 'anomaly'] = 1
            forecasted.loc[forecasted['actual'] <
                           forecasted['yhat_lower'], 'anomaly'] = 1

            forecasted['high_anomaly'] = (
                forecasted['actual'] - forecasted['yhat_upper']) / forecast['actual']
            forecasted['low_anomaly'] = (
                forecasted['yhat_lower'] - forecasted['actual']) / forecast['actual']
            forecasted['importance'] = forecasted.apply(
                lambda row: row['high_anomaly'] if row['anomaly'] == 1 else (
                    row['high_anomaly'] + row['low_anomaly']) / 2,
                axis=1)
            forecasted['importance'] = forecasted.apply(
                lambda row: row['low_anomaly'] if row['anomaly'] == -1 else row['importance'], axis=1)

            return forecasted

        except:
            print("Something went wrong when predicting anomalies.")

    def get_anomalies(self, model_result, bound_coefficients):
        """ Tries to predict anomalies based on training results for each coefficients.
        Args:
            model_result (Dataframe): The results of the training
            bound_coefficients (list): list of optimization coefficients for anomaly number
        Returns:
            anomaly_table (Dataframe): Anomaly numbers vs coefficients in dataframe
            anomaly_results (dict): Anomalies vs to coefficient values
        """
        try:
            number_of_anomalies = []
            anomaly_results = {}
            for coeff in bound_coefficients:
                forecast_result = self.train_forecast(
                    model_result, coeff)
                anomalies = forecast_result[forecast_result.anomaly.isin(
                    [-1, 1])]
                number_of_anomalies.append(len(anomalies))
                anomaly_results['{0}_anomaly_result'.format(coeff)] = anomalies

            return pd.DataFrame(list(zip(bound_coefficients, number_of_anomalies)),
                                columns=['coeff', 'anomaly_number']), anomaly_results

        except:
            print(
                "Something went wrong when predicting anomalies for each coeffcients.")

    def find_optimum_anomalies(self, anomaly_table, results):
        """ Tries to find best coefficient for getting optimum anomalies.
        Args:
            anomaly_table (Dataframe): Anomaly numbers vs coefficients in dataframe
            results (dict): Anomalies vs to coefficient values
        Returns:
            results (Dataframe): Detected optimum anomalies
        """
        try:
            anomaly_table["slope"] = (anomaly_table["anomaly_number"].diff().fillna(
                0.0) / anomaly_table["coeff"].diff().fillna(0.0)).fillna(0.0)
            best_coeff = anomaly_table[anomaly_table.slope ==
                                       anomaly_table.slope.min()]["coeff"].values[0]
            return results['{0}_anomaly_result'.format(best_coeff)]

        except:
            print(
                "Something went wrong when finding optimumu anomalies.")
