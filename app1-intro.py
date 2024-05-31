# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import requests
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer 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"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
data = query("Can you please let us know more details about your ")

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.H1(children=data),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)

