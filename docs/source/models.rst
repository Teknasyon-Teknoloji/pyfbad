Models
=====

pyfbad.models.models.IsolationForestModel
----------------------------------
That model includes classic Isolation Forest (IF) Model. It has **train_model()** method

   >>> train_model(self, df_model, contamination_value=float(0.06)) 
It has default contamination value (float(0.06)) and it trains the model and make prediction with given dataframe.

pyfbad.models.models.LocalOutlierFactorModel
--------------------------------------
That model includes classic Isolation Forest (IF) Model. It has **train_model()** method

   >>> train_model(self, df_model, contamination_value=float(0.06)) 
It has default contamination value (float(0.06)) and it trains the model and make prediction with given dataframe.

pyfbad.models.models.ProphetModel
---------------------------
That model developed by facebook and that is our first model we implemented on pyfbad.

   >>> train_model(self, df_model)
Train a Prophet model with given dataframe

   >>> train_forecast(self, forecast, bound_coefficient)
Tries to predict anomalies based on training results. 
**bound_coefficient (float):** optimization coefficient for anomaly number

   >>> get_anomalies(self, model_result, anomaly_number_level="Low")
Tries to predict anomalies based on number level for each coefficients.
**anomaly_number_level (str):** detected total anomaly number, high or low 

   >>> find_optimum_anomalies(self, anomaly_table, results):
Tries to find best coefficient for getting optimum anomalies.

pyfbad.models.models.GaussianMixtureModel
----------------------------------

   >>> train_model(self, df_model, cluster_number, random_state=7)
Train a Gaussian Mixture model with given dataframe.

   >>> get_all_models(self, data)
Train a Gaussian Mixture model with different cluster number values.

   >>> find_best_model(self, bic_table, models)
Find best gmm model wit respect to different cluster numbers.

   >>> train_forecast(self, gmm_model, model_data, anomaly_percent)
Forecasting anomalies using found best gmm model.
**anomaly_percent (int):** threshold value for number of detected anomalies 

.. autosummary::
   :toctree: generated

   PYFBAD
