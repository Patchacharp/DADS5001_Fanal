# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/cereal_data.csv?raw=True')

fig1 = px.scatter(df,
                x='sugars',
                y='rating',
                hover_name='name',
                title='Cereal ratings vs. sugars')

fig2 = px.histogram(df, x='sugars', title='Rating distribution')


app.layout = html.Div([ 

    html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph1',
            figure=fig1
        )

    ], style={'padding': 10, 'flex': 1}),

    html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph2',
            figure=fig2
        ),

        dcc.Slider(
            1,
            10,
            step=None,
            value=3,
            marks={str(i): str(i) for i in range(11)},
            id='nbin-slider'
        )

    ], style={'padding': 10, 'flex': 1})

 ], style={'display': 'flex', 'flexDirection': 'row', 'flex-wrap': 'wrap'})


@app.callback(
    Output('example-graph2', 'figure'),
    Input('nbin-slider', 'value'))
def update_figure(x): #x อาจเปลี่ยนเป็น slider_value
    fig2 = px.histogram(df, x='sugars', title='Rating distribution',nbins=x) #ถ้าเปลี่ยนชื่อ x เป็น slider_value ต้องเปลี่ยน x ใน nbins ด้วย
    fig2.update_layout(transition_duration=500)
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)

# https://www.g-able.com/digital-review/how-flexbox-help-to-make-website/
# https://medium.com/siamhtml/css-flexbox-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3-%E0%B8%AA%E0%B8%AD%E0%B8%99%E0%B8%A7%E0%B8%B4%E0%B8%98%E0%B8%B5%E0%B9%83%E0%B8%8A%E0%B9%89-a2100b93efff
