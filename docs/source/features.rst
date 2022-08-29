Features
=========

pyfbad.features.create_feature.Features
----------------------------------------

  >>> transform_data(self, df, time_column_name, value_column_name, filter=None)
Returns a two column dataframe ready to use train model.

**df (Dataframe):** A data frame contains a bunch of column

**time_column_name (str):** The column name will be defined time axis

**value_column_name (str):** The column name will be used as main data to train

**filter (list):** To takes only this "value" from the "column_name" --> ['country','TR'] 

  >>> extract_time_features(self, df_)
Create extra features from date value in dataframe.

  >>> get_modeling_data(self, df_model, model_name, date_type="D")
Returns a dataframe with extracted time features for modeling.

**df_model (Dataframe):** dataframe ready to use train model 

**model_name (str):** name of the model, IF or GMM 

**date_type (str):** data time range type, daily or hourly

