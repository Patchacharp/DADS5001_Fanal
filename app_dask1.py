# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, dcc, html
import plotly.express as px
import dask.dataframe as dd
import pandas as pd
import time
 
app = Dash(__name__)
 
#
start = time.time()
df = dd.read_csv("/Users/patcha/Desktop/Patcha/DADS Mac/2:2566/DADS5001/Week12/train_credit_bureau_a_2_5.csv")
end = time.time()
print(end - start) #pandas 0.002 sec, dask =  sec
 
#print(df.shape[0].compute())
print(df.head())
print(df["case_id"].nunique().compute()) #231250
pandas_df = df.compute() # convert to pandas
print(pandas_df.shape)
 
def filter_df(pop_thresh):
    filt_df = df[df["population"] > pop_thresh].compute()  # Note the use of .compute() function
    return filt_df
 
def build_graphs():
    pop_thresh = 5 * 10 ** 6
    filt_df = filter_df(pop_thresh)
 
    fig_out = px.scatter(filt_df, x="gdp per capita", y="life expectancy",
                         size="population", color="continent", hover_name="country",
                         log_x=True, size_max=60)
    return fig_out
 
'''
fig = build_graphs()
 
app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])
'''
if __name__ == '__main__':
    app.run(debug=True)