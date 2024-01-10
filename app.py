import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.offline as pyo

# Load CSV data and wrangle into format to create plots
df = pd.read_csv('traffic/views.csv')
df['Date'] = pd.to_datetime(df['_date'])
start_date = min(df['Date'])
end_date = max(df['Date'])
date_range = pd.date_range(start=start_date, end=end_date)
date_df = pd.DataFrame({'Date': date_range})
df = pd.merge(date_df, df, on='Date', how='left').fillna(0)
df['Total Views'] = pd.to_numeric(df['total_views'])
df['Unique Views'] = pd.to_numeric(df['unique_views']) 

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
    [Input('views-line-chart', 'relayoutData')] 
)
def update_chart(relayoutData):
    # Create figure
    fig = px.line(df, x='Date', y=['Total Views', 'Unique Views'],
                  labels={'value': 'Views', 'Date': 'Date'},
                  title='Views Over Time',
                  line_shape='spline') 

    # Fill the area under the 'Total Views' line with NHS blue
    fig.update_traces(fill='tozeroy', fillcolor='rgba(0,94,184,0.65)',
                      line=dict(color='#005EB8', width=2),  
                      selector=dict(name='Total Views'))

    # Fill the area under the 'Unique Views' line with NHS dark blue
    fig.update_traces(fill='tozeroy', fillcolor='rgba(0,48,135,0.65)',
                      line=dict(color='#003087', width=2),
                      selector=dict(name='Unique Views'))

    # Customise figure
    fig.update_layout(font=dict(family='Arial', size=12, color='black'),
                      legend=dict(x=0, y=1, traceorder='normal', orientation='v', title_text=''),
                      plot_bgcolor='rgba(0,0,0,0)', xaxis_title='', yaxis_title='', title='',
                      margin=dict(l=0, r=0, t=0, b=0))

    return fig

# Callback to update the bar chart
@app.callback(
    Output('avg-views-by-day-bar-chart', 'figure'),
    [Input('views-line-chart', 'relayoutData')]
)
# Create graph of average views per day of the week
def update_avg_views_chart(relayoutData):
    # Group by day of the week and calculate the average views
    avg_views_by_day = df.groupby(df['Date'].dt.day_name())[['Total Views']].mean()

    # Specify the order of days of the week and reorder the index
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_views_by_day = avg_views_by_day.reindex(days_order)

    # Create figure
    fig = px.bar(avg_views_by_day, x=avg_views_by_day.index, y='Total Views',
                 labels={'Total Views': 'Average Views', 'index': 'Day of the Week'},
                 title='Average Views by Day of the Week',
                 color_discrete_sequence=['#005EB8'])

    # Customise plot
    fig.update_layout(font=dict(family='Arial', size=12, color='black'),
                      xaxis_title='', yaxis_title='', plot_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(tickfont=dict(size=14)),
                      bargap=0.01, bargroupgap=0.1, title='',
                      margin=dict(l=0, r=0, t=0, b=0) )

    return fig

# Generate figures
views_line_chart = update_chart(None)
avg_views_by_day_bar_chart = update_avg_views_chart(None)

# Save as HTML files
pyo.plot(views_line_chart, filename="images/views_by_date.html", auto_open=False)
pyo.plot(avg_views_by_day_bar_chart, filename="images/views_by_day_average.html", auto_open=False)

# Run the app - uncomment this if you want the app to run, but be aware the GitHub action won't work properly with this.
#if __name__ == '__main__':
#   app.run_server(debug=True)