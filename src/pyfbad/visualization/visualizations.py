import plotly.graph_objects as go

class Anomaly_Visualization:

    def line_graph(self, df, value_column="y",layout=None):
        """It shows outliers on a time-series line graph as red marks
        Args:
            df (Dataframe): It contains modeled dataframe
            value_column (str): It represents counted value column's name
            layout (dictionary): If you want to make setting on line-graph, you can add it with values you want.
        Returns:
            It returns a marked time-series line-graph.
        """
        anomaly_points = df.loc[df['anomaly_score'] == 1]
        #Plot the actuals points
        actuals = go.Scatter(name = 'Actuals',
                             x = df.index,
                             y = df[value_column],
                             mode = 'lines',
                             marker = dict(size=12,
                                         line = dict(width=1),
                                         color = "blue"))

        #Highlight the anomaly points
        anomalies_map = go.Scatter(name = "Anomaly",
                                   showlegend = True,
                                   x = anomaly_points.index,
                                   y = anomaly_points[value_column],
                                   mode = 'markers',
                                   marker = dict(color = "red",
                                               size = 11,
                                               line = dict(
                                                   color = "red",
                                                   width = 2)))
        
        if layout != None:
            fig = go.Figure(data = [anomalies_map, actuals], layout = layout)
            
            return fig.show()
        
        fig = go.Figure(data = [anomalies_map, actuals])
        
        return fig.show()