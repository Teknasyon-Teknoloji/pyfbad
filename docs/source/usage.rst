Usage
=====

.. _installation:

Installation
------------

To use PYFBAS, first install it using pip:

.. code-block:: console

   (.venv) $ pip install pyfbad

Importing Libraries
----------------
>>> from pyfbad.data import database as db
>>> from pyfbad.features import create_feature as cf
>>> from pyfbad.models import models as md
>>> from pyfbad.visualization import visualizations as viz

Data Reading
----------------
>>> conn=db.File()
>>> df=conn.read_from_csv(time_column_name="timestamp", file_path="Twitter_volume_AMZN.csv")

Data Feature Extraction
----------------
>>> cf_obj = cf.Features()
>>> df_transform = cf_obj.transform_data(df=df, time_column_name="timestamp", 
                value_column_name="value")

>>> df_model = cf_obj.get_modeling_data(df_model=df_transform, model_name="IF", date_type='H')

**date_type** parameter gives the time grain 'H' means 'hourly', 'D' means 'daily' grain
**model_name** parameter gives spesific needs for spesific model

Data Modeling
----------------
>>> model_obj = md.IsolationForestModel()
>>> anomalies = model_obj.train_model(df_model = df_model, contamination_value=float(0.06))

Anomaly Visualization
----------------
>>> av = viz.Anomaly_Visualization()
>>> av.line_graph(anomalies, algorithm = "IF", time_column="ds", value_column="y", layout=None, save=False, path = None)
