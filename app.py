import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSV data
df = pd.read_csv('traffic/views.csv')
df['Date'] = pd.to_datetime(df['_date'])
df['Total Views'] = df['total_views']
df['Unique Views'] = df['unique_views']

# Create Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Views Over Time"),
    
    dcc.Graph(id='views-line-chart')
])

# Callback to update the chart
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
    fig.update_traces(fill='tozeroy', fillcolor='#005EB8',line=dict(color='#005EB8'), selector=dict(name='Total Views'))

    # Fill the area under the 'Unique Views' line with NHS dark blue
    fig.update_traces(fill='tozeroy', fillcolor='#003087', line=dict(color='#003087'), selector=dict(name='Unique Views'))

    # Customize legend
    fig.update_layout(legend=dict(title_text='Key'),
    plot_bgcolor= 'rgba(0,0,0,0)')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)