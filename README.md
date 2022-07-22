pyfbad
==============================

**Deployment & Documentation**

.. image:: https://img.shields.io/badge/pypi-v0.2.0-brightgreen
   :target: https://pypi.org/project/pyfbad/
   :alt: PyPI version

-----

The pyfbad library supports anomaly detection projects. An end-to-end anomaly detection application can be written using the source codes of this library only.

Given below is a basic application. Each module has more alternatives as follows;

• Database module -> Relational databases-(PostgreSQL,MySQL, etc.), NoSQL-(MongoDB) database or Cloud-(BigQuery)

• Models module   -> IsolationForest, LocalOutlierFactor, Prophet, GaussianMixtureModel

• Notification module -> Slack

**Installation**:

Python 2 is no longer supported. Make sure Python3.7+ is used as the programming language. The optimal version would be Python 3.7. It is recommended to use **pip** or **conda** for installation. Please make sure
**the latest version** is installed, as pyfbad is updated frequently:

    pip install pyfbad            # normal install
    pip install --upgrade pyfbad  # or update if needed

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
