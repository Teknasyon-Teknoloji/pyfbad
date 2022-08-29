Visualization
==============

pyfbad.visualizatin.visualizations.Anomaly_Visualization
---------------------------------------------------------

  >>> line_graph(self, df, algorithm, time_column="ds", value_column="y", layout=None, save=False, path=None)
It shows outliers on a time-series line graph as red marks.

**df (Dataframe):** It contains modeled dataframe

**algorithm (str):** name of the ML algorithm such as Isolation Forest, Prophet etc.

**time_column (str):** It represents column name of dates in dataset

**value_column (str):** It represents counted value column's name

**layout (dictionary):** If you want to make setting on line-graph, you can add it with values you want.
