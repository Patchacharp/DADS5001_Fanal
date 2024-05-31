#Reference: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash%20Components/Graph/dash-graph.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets) #ไปใช้ design จากข้างนอก

app.layout = html.Div([ #Div หน้าต่างใหญ่

    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True, options=[{'label': x, 'value': x} for x in df.country.unique()]), #id คือตั้งชื่อให้มัน
    html.Div([ #Divที่อยู่ใน Div
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='line-graph', figure={}, clickData=None, hoverData=None, #hover เมาท์อยู่บนแต่ยังไม่คลิก
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': False,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  ),
        dcc.Graph(id='bar-graph', figure={}, className='six columns')   
    ])
])

@app.callback( #ฝั่งขวา
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(country_chosen): #check ว่าอยู่ใน dff หรือป่าว
    dff = df[df.country.isin(country_chosen)]
    #print(dff)
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country',  hover_data=["lifeExp", "pop", "iso_alpha"])
    fig.update_traces(mode='lines+markers') #มีเส้นและจุด
    return fig

# Dash version 1.16.0 or higher 
@app.callback( #ฝั่งซ้าย ต้องทำให้เปลี่ยนตามที่คลิกฝั่งขวา
    Output(component_id='pie-graph', component_property='figure'),
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id='line-graph', component_property='hoverData'),
    Input(component_id='line-graph', component_property='clickData'),
    Input(component_id='line-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen): #ต้องเรียงตามมาอะไรมาก่อน hov มาclick มาselect มาcheck country
    if hov_data is None: #ถ้าไม่ hov ให้โชว์ default ตามที่เราตั้ง
        dff2 = df[df.country.isin(country_chosen)]
        dff2 = dff2[dff2.year == 1952]
        #print(dff2)
        fig2 = px.pie(data_frame=dff2, values='pop', names='country',
                      title='Population for 1952')
        fig3 = px.bar(data_frame=dff2, x='country', y='gdpPercap', color='country',  hover_data=["lifeExp", "pop", "iso_alpha"])
        return fig2, fig3
    else: #ถ้ามีการ hov
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        print(f'click data: {clk_data}')
        print(f'selected data: {slct_data}')
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = hov_data['points'][0]['x'] #hov คือขอเข้าไปที่ x (ปี) ถ้าอยากเข้าไปที่ GDP ให้เข้าไป y แทน
        dff2 = dff2[dff2.year == hov_year] #เอาปีมา filter
        fig2 = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}')
        fig3 = px.bar(data_frame=dff2, x='country', y='gdpPercap', color='country',  hover_data=["lifeExp", "pop", "iso_alpha"])
        return fig2, fig3

if __name__ == '__main__':
    app.run_server(debug=True)

'''
GDP Per Capita คือ ผลิตภัณฑ์มวลรวมในประเทศต่อหัว หรือ GDP ต่อหัว 
เป็นตัวเลขที่บอกว่าค่าเฉลี่ยของ GDP เมื่อเทียบกับคนในประเทศแล้ว โดยเฉลี่ยคนหนึ่งคนสามารถสร้างมูลค่า GDP ขึ้นมาเท่าไหร่ 
และแน่นอนว่า GDP per capita คือ ตัวเลขที่คำนวณมาจาก ค่า GDP ÷ จำนวนประชากร

iso_alpha
The 3-letter ISO 3166-1 alpha-3 code.

iso_num
The 3-digit ISO 3166-1 numeric-3 code.

อายุคาดเฉลี่ย (Life Expectancy) : LE หรือ Life Expectancy หมายถึง
การคาดประมาณจำนวนปีโดยเฉลี่ยของการมีชีวิตอยู่ของประชากร
'''

