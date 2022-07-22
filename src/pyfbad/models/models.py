from prophet import Prophet
from sqlalchemy import *
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
import pandas as pd


class IsolationForestModel:

    def train_model(self, df_model, contamination_value=float(0.06)):
        """ Train a Isolation Forest model and make prediction with given dataframe.
        Args:
            df_model (Dataframe): Dataframe ready to use train model 
            contamination_value (float): It contains default float value for contamination parameter
        Returns:
            df_model (Dataframe): The results of the anomaly forecasting
        """
        try:
            df_columns = df_model.columns
            model = IsolationForest(n_estimators=100,
                                    max_samples='auto',
                                    contamination=contamination_value,
                                    random_state=41)
            model.fit(df_model[df_columns])
            df_model['score'] = model.decision_function(df_model[df_columns])
            df_model['anomaly'] = model.predict(df_model[df_columns])
            df_model['anomaly'][df_model['anomaly'] == 1] = 0
            df_model['anomaly'][df_model['anomaly'] == -1] = 1
            return df_model.reset_index()[["ds", "y", "score", "anomaly"]]
        except Exception:
            raise Exception(
                "Error when the IF model training and prediction...")


class LocalOutlierFactorModel:

    def train_model(self, df_model, contamination_value=float(0.06)):
        """ Train a Local Outlier Factor model and make prediction with given dataframe.
        Args:
            df_model (Dataframe): Dataframe ready to use train model 
            contamination_value (float): It contains default float value for contamination parameter
        Returns:
            df_model (Dataframe): The results of the anomaly forecasting
        """
        try:
            # building model object
            model = LocalOutlierFactor(contamination=contamination_value)
            # model fitting and prediction
            df_model["anomaly"] = model.fit_predict(df_model)
            df_model['anomaly'][df_model['anomaly'] == 1] = 0
            df_model['anomaly'][df_model['anomaly'] == -1] = 1
            return df_model.reset_index()[["ds", "y", "anomaly"]]
        except Exception:
            raise Exception(
                "Error when the LOF model training and prediction...")


class ProphetModel:

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
        except Exception:
            raise Exception("Error when the prophet model training...")

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

            forecasted['yhat_upper'] = forecasted['yhat_upper'] * \
                bound_coefficient
            forecasted['yhat_lower'] = forecasted['yhat_lower'] / \
                bound_coefficient
            forecasted['anomaly'] = forecasted.apply(lambda row: 1 if (row['actual'] < row['yhat_lower']) | (
                row['actual'] > row['yhat_upper']) else 0, axis=1)
            forecasted['anomaly'] = forecasted.apply(lambda row: 1 if
                                                     (row['actual'] < row['yhat_lower']) |
                                                     (row['actual'] > row['yhat_upper']) else 0, axis=1)
            return forecasted
        except Exception:
            raise Exception("Error when predicting anomalies...")

    def get_anomalies(self, model_result, anomaly_number_level="Low"):
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
                anomaly_results['{0}_anomaly_result'.format(
                    coeff)] = forecast_result
            return pd.DataFrame(number_of_anomalies,
                                columns=['coeff', 'anomaly_number']), anomaly_results
        except Exception:
            raise Exception(
                "Error when predicting anomalies for each coeffcients...")

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
            return results['{0}_anomaly_result'.format(best_coeff)][["ds", "actual", "anomaly"]] \
                .rename(columns={"actual": "y"})
        except Exception:
            raise Exception("Error when finding optimum anomalies...")


class GaussianMixtureModel:

    def train_model(self, df_model, cluster_number, random_state=7):
        """ Train a Gaussian Mixture model with given dataframe.
        Args:
            df_model (Dataframe): dataframe ready to use train model 
            cluster_number (int): number of clusters that used in gmm model
            random_state (int): random state value to provide constant results
        Returns:
            df_model (Dataframe): feature extacted dataframe
            gmm model (model): fitted gmm model
        """
        try:
            df_model = df_model.reset_index()
            model = GaussianMixture(
                n_components=cluster_number, random_state=random_state)
            return df_model, model.fit(df_model.drop("ds", axis=1))
        except Exception:
            raise Exception("Error when training gmm model...")

    def get_all_models(self, data):
        """ Train a Gaussian Mixture model with different cluster number values.
        Args:
            data (Dataframe): dataframe ready to use train model 
        Returns:
            bic_table (Dataframe): cluster number vs bic value dataframe
            all_models (dict): dictionary that contains all gmm models vs cluster number
        """
        try:
            bic_values = []
            all_models = {}
            cluster_numbers = list(np.arange(1, 10))
            for n in cluster_numbers:
                df, model = self.train_model(data.copy(), n)
                bic_values.append(
                    [n, round(model.bic(df.drop("ds", axis=1)), 4)])
                all_models['{0}_trained_model'.format(n)] = model, df
            return pd.DataFrame(bic_values,
                                columns=['cluster', 'BIC']), all_models
        except Exception:
            raise Exception("Error when getting all gmm models...")

    def find_best_model(self, bic_table, models):
        """ Find best gmm model wit respect to different cluster numbers.
        Args:
            bic_table (Dataframe): cluster number vs bic value dataframe
            models (dict): dictionary that contains all gmm models vs cluster number
        Returns:
            best model (model): detected best model
            model data (Dataframe): dataframe that used in modelling
        """
        try:
            best_cluster = bic_table[bic_table.BIC ==
                                     bic_table.BIC.min()]["cluster"].values[0]
            return models['{0}_trained_model'.format(best_cluster)]
        except Exception:
            raise Exception("Error when finding best gmm model...")

    def train_forecast(self, gmm_model, model_data, anomaly_percent):
        """ Forecasting anomalies using found best gmm model.
        Args:
            gmm_model (model): detected best model 
            model_data (Dataframe): dataframe that used in modelling
            anomaly_percent (int): threshold value for number of detected anomalies 
        Returns:
            anomaly_results (Dataframe): dataframe that contains anomaly forecasting
        """
        try:
            scores = gmm_model.score_samples(model_data.drop("ds", axis=1))
            model_data["score"] = scores
            model_data['anomaly'] = model_data['score'].apply(
                lambda x: 1 if x < np.percentile(scores, anomaly_percent) else 0)
            return model_data[["ds", "y", "score", "anomaly"]]
        except Exception:
            raise Exception("Error when forecasting anomalies...")
