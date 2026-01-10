"""
Plotly-based interactive SPC chart renderer.
Provides web-ready, interactive control charts using Plotly.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shortuuid

from .spc import Spc, CHART_X_MR_X


class PlotlySpcChart:
    """
    Creates interactive SPC charts using Plotly.

    Args:
        data: List of data points or list of lists for subgrouped data
        title: Chart title
        chart_type: Type of SPC chart (defaults to CHART_X_MR_X)
        sizes: Subgroup size (optional)

    Example:
        >>> data = [1,2,3,4,5,6,7,8,9,8,7,6,5,5,5,4,4,3,3,2,2,2,3,4,5,5,5]
        >>> chart = PlotlySpcChart(data, title="Widget Quality")
        >>> html = chart.render_to_html()
    """

    def __init__(self, data, title=None, chart_type=CHART_X_MR_X, sizes=None):
        self.data = data
        self.title = title or "SPC Chart"
        self.chart_type = chart_type
        self.sizes = sizes

        # Calculate SPC statistics
        self.spc = Spc(data, chart_type, sizes=sizes)
        self.center, self.lcl, self.ucl = self.spc.get_stats()
        self.violations = self.spc.get_violating_points()

    def render_to_html(self, include_plotlyjs=True):
        """
        Render the chart to HTML string.

        Args:
            include_plotlyjs: Whether to include plotly.js in output (default True)

        Returns:
            HTML string containing the interactive chart
        """
        fig = self._create_figure()

        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'spc_chart_{shortuuid.uuid()}',
                'height': 600,
                'width': 1200,
                'scale': 2
            }
        }

        html = fig.to_html(
            include_plotlyjs=include_plotlyjs,
            config=config
        )

        return html

    def render_to_file(self, filename=None):
        """
        Render the chart to an HTML file.

        Args:
            filename: Output filename (defaults to auto-generated)

        Returns:
            Path to the created file
        """
        if filename is None:
            filename = f"spc_chart_{shortuuid.uuid()}.html"

        fig = self._create_figure()
        fig.write_html(filename)

        return filename

    def _create_figure(self):
        """Create the Plotly figure with SPC data."""
        fig = go.Figure()

        # X-axis values (index of data points)
        x_values = list(range(1, len(self.data) + 1))

        # Add control limits (only if they exist)
        if self.ucl is not None:
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[self.ucl] * len(self.data),
                mode='lines',
                name='UCL (Upper Control Limit)',
                line=dict(color='red', width=2, dash='dash'),
                hovertemplate='UCL: %{y:.3f}<extra></extra>'
            ))

        if self.lcl is not None:
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[self.lcl] * len(self.data),
                mode='lines',
                name='LCL (Lower Control Limit)',
                line=dict(color='red', width=2, dash='dash'),
                hovertemplate='LCL: %{y:.3f}<extra></extra>'
            ))

        # Add center line
        fig.add_trace(go.Scatter(
            x=x_values,
            y=[self.center] * len(self.data),
            mode='lines',
            name='Center Line',
            line=dict(color='green', width=2, dash='dot'),
            hovertemplate='Center: %{y:.3f}<extra></extra>'
        ))

        # Determine which points are violations
        violation_indices = set()
        for rule, indices in self.violations.items():
            violation_indices.update(indices)

        # Split data into normal and violation points
        normal_x = []
        normal_y = []
        violation_x = []
        violation_y = []

        for i, value in enumerate(self.data):
            if i in violation_indices:
                violation_x.append(i + 1)
                violation_y.append(value)
            else:
                normal_x.append(i + 1)
                normal_y.append(value)

        # Add normal data points
        if normal_x:
            fig.add_trace(go.Scatter(
                x=normal_x,
                y=normal_y,
                mode='lines+markers',
                name='Data Points',
                line=dict(color='blue', width=2),
                marker=dict(size=8, color='blue'),
                hovertemplate='Point %{x}: %{y:.3f}<extra></extra>'
            ))

        # Add violation points
        if violation_x:
            fig.add_trace(go.Scatter(
                x=violation_x,
                y=violation_y,
                mode='markers',
                name='Violations',
                marker=dict(size=12, color='orange', symbol='x'),
                hovertemplate='Point %{x}: %{y:.3f}<br>Violation!<extra></extra>'
            ))

        # Update layout
        fig.update_layout(
            title={
                'text': self.title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Sample Number',
            yaxis_title='Value',
            hovermode='closest',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )

        # Add range slider
        fig.update_xaxes(rangeslider_visible=True)

        return fig

    def get_figure(self):
        """
        Get the Plotly figure object for further customization.

        Returns:
            plotly.graph_objects.Figure
        """
        return self._create_figure()
