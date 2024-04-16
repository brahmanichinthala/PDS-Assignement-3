import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd

# JSONPlaceholder API endpoint
base_url = 'https://jsonplaceholder.typicode.com/users'

# Initialize Dash app
app = dash.Dash(__name__)

# Define styles
styles = {
    'container': {
        'width': '80%',
        'margin': 'auto',
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '5px',
        'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)',
        'background-color': '#f9f9f9'
    },
    'table': {
        'border-collapse': 'collapse',
        'width': '100%',
        'margin-top': '20px'
    },
    'th': {
        'border': '1px solid #ddd',
        'padding': '10px',
        'text-align': 'left',
        'background-color': '#f2f2f2',
        'padding-left': '20px',
        'color': '#333'
    },
    'td': {
        'border': '1px solid #ddd',
        'padding': '10px',
        'color': '#666'
    }
}

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Users Dashboard", style={'text-align': 'center', 'color': '#444', 'margin-bottom': '20px'}),
    html.Div(id='user-output', style=styles['container'])
])

# Callback to fetch and display random user data in a table
@app.callback(
    Output('user-output', 'children'),
   [Input('user-output', 'children')]
)
def update_users_table(n_clicks):
    # Make request to JSONPlaceholder API
    response = requests.get(base_url)

    if response.status_code == 200:
        users_data = response.json()[:50]  # Assuming we want the first 5 users from the response

        # Convert user data to DataFrame for easier manipulation
        df = pd.DataFrame(users_data)
        df = df.drop(columns=['address', 'company'])

        # Display user information in a table
        table_header = [html.Th(col, style=styles['th']) for col in df.columns]
        table_rows = []
        for _, row in df.iterrows():
            row_data = [html.Td(str(row[col]), style=styles['td']) for col in df.columns]
            table_rows.append(html.Tr(row_data))

        user_table = html.Table([
            html.Thead(html.Tr(table_header)),
            html.Tbody(table_rows)
        ], style=styles['table'])
        return user_table
    else:
        return html.P("Failed to fetch user data.")

if __name__ == '__main__':
    app.run_server(debug=True)
