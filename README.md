pyfbad
==============================

The pyfbad library supports anomaly detection projects. An end-to-end anomaly detection application can be written using the source codes of this library only.

Given below is a basic application. Each module has more alternatives as follows;
• Database module -> Relational databases (PostgresSQL,MySQL, etc.), NoSQL(MongoDB) database or Cloud (BigQuery)
• Models module   -> IsolationForest, LocalOutlierFactor, Prophet, GaussianMixtureModel
• Notification module -> Slack

**Installation**:

Python 2 is no longer supported. Make sure Python3+ is used as the programming language. The optimal version would be Python 3.7. It is recommended to use **pip** or **conda** for installation. Please make sure
**the latest version** is installed, as pyfbad is updated frequently:

    pip install pyfbad            # normal install
    pip install --upgrade pyfbad  # or update if needed

**Database Operations - Read From MongoDB**:

    # connect to mongodb
    from pyfbad.data import database as db
    database_obj = db.MongoDB('db_name', PORT, 'db_path')
    database = database_obj.get_mongo_db()

    # check the collections
    collections = dataset_obj.get_collection_names(database)

    # build mongodb query
    filter = dataset_obj.add_filter(
    [],
    'time',
    {
        "column_name": "datetime",
        "date_type": "hourly",
        "start_time": "2019-02-06 00:00:00",
        "finish_time": "2019-10-06 00:00:00"
    })

    # get data from db as dataframe
    data = dataset_obj.get_data_as_df(
        database=database,
        collection=collections[0],
        filter=filter
    )
**Database Operations - Read From File**:

    from pyfbad.data import database as db
    conn=db.File()
    df=conn.read_from_csv(time_column_name="timestamp", file_path="Twitter_volume_AMZN.csv")

**Database Operations - Read From BigQuery**:

    # connect to BigQuery
    from pyfbad.data import database as db
    conn=db.CloudDB(key_path, project_name)
    df=conn.reading_raw_data(query_string)

    # After training a model
    writing_to_bq(dataframe, dataset, table_name)

**Database Operations - Read From SQLDB**:

    # connect to SQL database
    from pyfbad.data import database as db
    parameters = {"db": "postgresql", "username": "postgres",
              "password": "mypassword", "host": '127.0.0.1', "port": 5444, "database": "test"}
    conn=db.SQLDB(**parameters)
    conn.set_db_conn()
    query = 'SELECT * FROM {0}'.format(table_name)
    data = conn.reading_rawdata(query, conn.create_db_conn(), table_name)

    # After training a model
    obj.writing_to_db(data, obj.create_db_conn(), table_name)

**Feature Operations**:

    from pyfbad.features import create_feature as cf
    cf_obj = cf.Features()
    df_transform = cf_obj.transform_data(df=df_, time_column_name="count_datetime", 
                    value_column_name="count", filter=['_id.country','TR'])

    df_model = cf_obj.get_modeling_data(df=df_transform, model_name="IF", date_type='D')

**Model Operations - ProphetModel**:

    from pyfbad.models import models as md
    model_obj = md.Model_Prophet()
    # detect anomalies for all coefficients
    table, results = model_obj.get_anomalies(model_result = model_obj.train_model(df_model), anomaly_number_level = "Low")
    # find optimum anomalies for best result
    anomalies = model_obj.find_optimum_anomalies(anomaly_table = table, results = results)

**Model Operations - IsolationForestModel**:

    from pyfbad.models import models as md
    model_obj = md.IsolationForestModel()
    # train IF model and detect anomalies by forecasting
    anomalies = model_obj.train_model(df_model = df_model, contamination_value=float(0.06))

**Model Operations - GaussianMixtureModel**:

    from pyfbad.models import models as md
    model_obj = md.GaussianMixtureModel()
    # train GMM models for all cluster numbers
    table, results = model_obj.get_all_models(data = df_model)
    # finds best GMM model and its data according to BIC values
    best_model, modeled_data = model_obj.find_best_model(bic_table = table, models = results)
    # detecting anomalies using best GMM model
    anomalies = model_obj.train_forecast(gmm_model = best_model, model_data = modeled_data, anomaly_percent = 6)

**Model Operations - LocalOutlierFactorModel**:

    from pyfbad.models import models as md
    model_obj = md.LocalOutlierFactorModel()
    # train LOF model and detect anomalies by forecasting
    anomalies = model_obj.train_model(df_model = df_model, contamination_value=float(0.06))

**Visualizations Operations**:

    from pyfbad.visualization import visualizations as vis
    av = vis.Anomaly_Visualization()
    av.line_graph(df_model, algorithm = "IF", time_column="ds", value_column="y", layout=None, save=True, path = None)

**Notification Operations**:

    from pyfbad.notification import notifications as nt
    gmail_obj = nt.Email()
    if 1 or -1 in anomaly_result['anomaly']:
        gmail_obj.send_gmail('sample_from@gmail.com','password','sample_to@gmail.com')

**Required Dependencies**:

Depencies can be shown in requirements.txt file.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   └── pyfbad
    │      ├── __init__.py    <- Makes pyfbad a Python module
    │      │
    │      ├── data           <- Scripts to read raw data from different sources
    │      │   └── database.py
    │      │   └── __init__.py
    │      │
    │      ├── features       <- Scripts to turn raw data into features for modeling
    │      │   └── create_feature.py
    │      │   └── __init__.py
    │      │
    │      ├── models         <- Scripts to train models and then use trained models to make
    │      │   │                 predictions for anomaly detection
    │      │   └── models.py
    │      │   └── __init__.py
    │      │
    │      │── notification  <- Scripts for setting up notification systems.
    │      │    └── notification.py
    │      │    └── __init__.py
    │      │
    │      └── visualization  <- Scripts for visualizing of detected anomalies
    │          └── visualizations.py
    │          └── __init__.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
