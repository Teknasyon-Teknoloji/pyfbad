from fbprophet import Prophet
from sqlalchemy import *
from sklearn.ensemble import IsolationForest
import pandas as pd


class Model_IsolationForest:

    def train_model(self, df_model, contamination_value, date_type=''):
        """ Train a Isolation Forest model with given dataframe.
        Args:
            df_model (Dataframe): Two column dataframe ready to use train model
            contamination_value (float): threshold to find optimum anomaly number
            date_type (str): date type of dataset, Hourly or Daily
        Returns:
            df_model (Dataframe): The results of the training
        """
        df_model['ds'] = pd.to_datetime(df_model['ds'])

        # set timestamp to index
        df_model.set_index('ds', drop=True, inplace=True)
        # resample timeseries to hourly
        if(date_type == "H"):
            df_model = df_model.resample('H').sum()
            df_model['hour'] = [i.hour for i in df_model.index]

        else:
            df_model = df_model.resample('D').sum()
        # creates features from date
        df_model['day'] = [i.day for i in df_model.index]
        df_model['month'] = [i.month for i in df_model.index]
        df_model['year'] = [i.year for i in df_model.index]
        df_model['day_of_year'] = [i.dayofyear for i in df_model.index]
        df_model['week_of_year'] = [i.weekofyear for i in df_model.index]
        df_model['is_weekday'] = [i.isoweekday() for i in df_model.index]

        model = IsolationForest(n_estimators=100, max_samples='auto',
                                contamination=contamination_value, random_state=41)

        model.fit(df_model[['y', 'day', 'month', 'year',
                  'day_of_year', 'week_of_year', 'is_weekday']])

        df_model['scores'] = model.decision_function(
            df_model[['y', 'day', 'month', 'year', 'day_of_year', 'week_of_year', 'is_weekday']])

        df_model['anomaly_score'] = model.predict(
            df_model[['y', 'day', 'month', 'year', 'day_of_year', 'week_of_year', 'is_weekday']])

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
                                   'yhat_lower', 'yhat_upper', 'actual']]

            forecasted['anomaly'] = 0
            forecasted['yhat_upper'] = forecasted['yhat_upper'] * \
                bound_coefficient
            forecasted['yhat_lower'] = forecasted['yhat_lower'] / \
                bound_coefficient
            forecasted.loc[forecasted['actual'] >
                           forecasted['yhat_upper'], 'anomaly'] = 1
            forecasted.loc[forecasted['actual'] <
                           forecasted['yhat_lower'], 'anomaly'] = 1
            return forecasted
        except:
            print("Something went wrong when predicting anomalies.")

    def get_anomalies(self, model_result, anomaly_number_level):
        """ Tries to predict anomalies based on number level for each coefficients.
        Args:
            model_result (Dataframe): The results of the training
            anomaly_number_level (str): detected total anomaly number, high or low 
        Returns:
            anomaly_table (Dataframe): Anomaly numbers vs coefficients in dataframe
            anomaly_results (dict): Anomalies vs to coefficient values
        """
        number_of_anomalies = []
        anomaly_results = {}
        bound_coefficients = {
            "High": [1.0, 0.9, 0.8, 0.7, 0.6], "Low": [1.0, 1.1, 1.2, 1.3, 1.4]}
        try:
            for coeff in bound_coefficients[anomaly_number_level]:
                forecast_result = self.train_forecast(model_result, coeff)
                anomalies = forecast_result[forecast_result["anomaly"] == 1]
                number_of_anomalies.append([coeff, len(anomalies)])
                anomaly_results['{0}_anomaly_result'.format(coeff)] = anomalies
            return pd.DataFrame(number_of_anomalies,
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
                "Something went wrong when finding optimum anomalies.")
