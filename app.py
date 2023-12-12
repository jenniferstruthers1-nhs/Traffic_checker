import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.offline as pyo

# Load CSV data
df = pd.read_csv('traffic/views.csv')
df['Date'] = pd.to_datetime(df['_date'])
df['Total Views'] = pd.to_numeric(df['total_views'])  # Ensure 'Total Views' is numeric
df['Unique Views'] = pd.to_numeric(df['unique_views'])  # Ensure 'Unique Views' is numeric

# Create Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Views Over Time"),

    dcc.Graph(id='views-line-chart'),

    html.Div([
        html.H2("Average Views by Day of the Week"),
        dcc.Graph(id='avg-views-by-day-bar-chart')
    ])
])

# Callback to update the line chart
@app.callback(
    Output('views-line-chart', 'figure'),
    [Input('views-line-chart', 'relayoutData')]  # Use a dummy input since no dropdown is used
)
def update_chart(relayoutData):
    fig = px.line(df, x='Date', y=['Total Views', 'Unique Views'],
                  labels={'value': 'Count', 'Date': 'Date'},  # Updated x-axis label
                  title='Views Over Time',
                  line_shape='linear')  # Ensure a linear shape for the line

    # Fill the area under the 'Total Views' line with NHS blue
    fig.update_traces(fill='tozeroy', fillcolor='#005EB8', line=dict(color='#005EB8'), selector=dict(name='Total Views'))

    # Fill the area under the 'Unique Views' line with NHS dark blue
    fig.update_traces(fill='tozeroy', fillcolor='#003087', line=dict(color='#003087'), selector=dict(name='Unique Views'))

    # Customize legend
    fig.update_layout(legend=dict(title_text='Key'),
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig

# Callback to update the bar chart
@app.callback(
    Output('avg-views-by-day-bar-chart', 'figure'),
    [Input('views-line-chart', 'relayoutData')]  # Use the same dummy input for simplicity
)
def update_avg_views_chart(relayoutData):
    # Group by day of the week and calculate the average views
    avg_views_by_day = df.groupby(df['Date'].dt.day_name())[['Total Views']].mean()

    # Specify the order of days of the week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Reorder the index
    avg_views_by_day = avg_views_by_day.reindex(days_order)

    fig = px.bar(avg_views_by_day, x=avg_views_by_day.index, y='Total Views',
                 labels={'Total Views': 'Average Views', 'index': 'Day of the Week'},
                 title='Average Views by Day of the Week',
                 color_discrete_sequence=['#FFC0CB'])

    # Update x-axis label, remove background
    fig.update_layout(xaxis_title='Day of the Week', plot_bgcolor='rgba(0,0,0,0)')

    return fig

# Generate figures
views_line_chart = update_chart(None)
avg_views_by_day_bar_chart = update_avg_views_chart(None)

# Save HTML files
pyo.plot(views_line_chart, filename="images/views_by_date.html", auto_open=False)
pyo.plot(avg_views_by_day_bar_chart, filename="images/views_by_day_average.html", auto_open=False)
