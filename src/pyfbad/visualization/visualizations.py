import plotly.graph_objects as go
import os


class Anomaly_Visualization:

    def line_graph(self, df, algorithm, time_column="ds", value_column="y", layout=None, save=False, path=None):
        """It shows outliers on a time-series line graph as red marks
        Args:
            df (Dataframe): It contains modeled dataframe
            algorithm (str): name of the ML algorithm such as Isolation Forest, Prophet etc.
            time_column (str): It represents column name of dates in dataset
            value_column (str): It represents counted value column's name
            layout (dictionary): If you want to make setting on line-graph, you can add it with values you want.
        Returns:
            It returns a marked time-series line-graph.
        """
        anomaly_points = df[df['anomaly'] == 1]
        # Plot the actuals points
        actuals = go.Scatter(name='Actuals',
                             x=df[time_column],
                             y=df[value_column],
                             mode='lines',
                             marker=dict(size=12,
                                         line=dict(width=1),
                                         color="blue"))
        # Highlight the anomaly points
        anomalies_map = go.Scatter(name="Anomaly",
                                   showlegend=True,
                                   x=anomaly_points[time_column],
                                   y=anomaly_points[value_column],
                                   mode='markers',
                                   marker=dict(color="red",
                                               size=11,
                                               line=dict(
                                                   color="red",
                                                   width=2)))
        fig = go.Figure(data=[anomalies_map, actuals], layout=layout)
        fig.update_layout(
            title_text='{0} Anomaly Detection Results'.format(algorithm), title_x=0.5)
        if save:
            if path:
                if not os.path.exists("{0}/plots".format(path)):
                    os.mkdir("{0}/plots".format(path))
                fig.write_image("{0}/plots/line_graph.png".format(path))
            else:
                if not os.path.exists("plots"):
                    os.mkdir("plots")
                fig.write_image("plots/line_graph.png")
        return fig.show()
