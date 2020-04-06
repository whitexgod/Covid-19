import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.express as px
import dash_table

# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]

covid_19_data=pd.read_csv('covid_19_data.csv')
us_cities=pd.read_csv('time_series_covid_19_deaths_US.csv')
world_c=pd.read_csv('time_series_covid_19_confirmed.csv')
world_c1=world_c[['Country/Region','Lat','Long']]
world_c1.rename(columns={'Country/Region':'Country_Region'},inplace=True)
world_c_US=pd.read_csv('time_series_covid_19_confirmed_US.csv')
world_c_US2=world_c_US[['Country_Region','Lat','Long_']]
world_c_US2.rename(columns={'Long_':'Long'},inplace=True)
world=world_c1.append(world_c_US2)



fig2 = px.scatter_mapbox(world, lat=world["Lat"], lon=world["Long"], hover_name=world["Country_Region"],
                        color_discrete_sequence=["fuchsia"], zoom=.5, height=600)
fig2.update_layout(title='The corona virus affected Countries around the World : ',
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])


fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon=us_cities["Long_"],
        lat=us_cities["Lat"],
        text=us_cities["Province_State"],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'Blues',
            cmin = 0,
            colorbar_title="The Deeper the colour the more affected the city is : "
        )))
fig.update_layout(
        title = 'The corona virus affected Cities in US -',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )



countries=covid_19_data['Country/Region'].unique().tolist()
total_c=[]
total_r=[]
total_d=[]
for i in countries:
    new_df=covid_19_data[covid_19_data['Country/Region']==i]
    if(new_df['Province/State'].count() == 0 ):
        count_c=new_df.drop_duplicates(subset='Country/Region',keep='last')['Confirmed'].sum()
        total_c.append(count_c)
        count_r=new_df.drop_duplicates(subset='Country/Region',keep='last')['Recovered'].sum()
        total_r.append(count_r)
        count_d=new_df.drop_duplicates(subset='Country/Region',keep='last')['Deaths'].sum()
        total_d.append(count_d)
    else:
        count_c=new_df.drop_duplicates(subset='Province/State',keep='last')['Confirmed'].sum()
        total_c.append(count_c)
        count_r=new_df.drop_duplicates(subset='Province/State',keep='last')['Recovered'].sum()
        total_r.append(count_r)
        count_d=new_df.drop_duplicates(subset='Province/State',keep='last')['Deaths'].sum()
        total_d.append(count_d)
total_confirmed=np.sum(total_c)
total_recovered=np.sum(total_r)
total_death=np.sum(total_d)
active_cases=total_confirmed-(total_recovered+total_death)
closed_cases=(total_recovered+total_death)

data11={'Countries': countries, 'Total cases' : total_c}
df11=pd.DataFrame(data11)
data22={'Countries': countries, 'Total cases' : total_r}
df22=pd.DataFrame(data22)
data33={'Countries': countries, 'Total cases' : total_d}
df33=pd.DataFrame(data33)

option=[
    {'label':'Infected', 'value':'Infected'},
    {'label':'Countries-Recovered','value':'total_recovered'}
]

options=[
   {'label':'All', 'value':'All'},
   {'label':'Total Recovered', 'value':'total_recovered'},
   {'label':'Total Confirmed', 'value':'total_confirmed'},
   {'label':'Total Death', 'value':'total_death'}
]


app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app2.server

app2.layout=html.Div([
    html.H5("updated on : 06/04/2020, Time : 11:00 ", style={ 'text-align':'right', 'padding':'1%', 'color':'#FFFFFF'}),
    html.H1("Corona Virus Pandemic Analysis", style={'text-align': 'center'}, className='title'),
    html.Img(className='image', src='https://cdn.kalingatv.com/wp-content/uploads/2020/03/Coronavirus-COVID-19.jpg', alt='covid-19 image',
             style={
                 'height': '400px',
                 'float': 'center',
                 'position': 'relative',}

             ),
    html.H4('The structure of a COVID-19 Virus',className='structure', style= {
                    'color' : '#fc172e',
                    'text-align' : 'center',
                    'font-size' : '2rem',
                    'font-weight' : 'bold',
                    'padding' : '1%',
    }),
    html.A("Link to external site- World Health Organization reports", href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019', target="_blank"),
    html.Hr(className='hrtag'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Img(className='title-image',
                             src="https://webassets.mongodb.com/_com_assets/cms/3D_medical_animation_coronavirus_structure-0kardto2r8.jpg",
                             alt='Picture of a covid 19 virus',
                             style={
                                 'height': '60%',
                                 'width': '60%',
                                 'float': 'left',
                                 'position': 'relative',
                                 'padding-top': 0,
                                 'padding-right': 0},
                             ),
                    html.P('People may be sick with the virus for 1 to 14 days before developing symptoms.'
                           ' The most common symptoms of coronavirus disease (COVID-19) are fever, tiredness, and dry cough. Most people (about 80%) '
                           'recover from the disease without needing special treatment.More rarely, the disease can be serious and even fatal. Older people, and people with other medical conditions '
                           '(such as asthma, diabetes, or heart disease), may be more vulnerable to becoming severely ill.', className='para'),
                    html.Hr(className='hrtag'),

                ],className='card-body')
            ],className='card')
        ],className='col-lg-12')
    ],className='row'),
    html.H3('Present Status Across the World :', className='title-bar', style= {
        'color':'#fc172e'
    }),
    html.Div([
        html.Div([
            html.Div([
                html.Div([

                    html.H3("Total Cases", style={'font-size':'20px'}),
                    html.H4(total_confirmed, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([

                    html.H3("Active Cases",style={'font-size':'20px'}),
                    html.H4(active_cases, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([

                    html.H3("Closed Cases", style={'font-size':'20px'}),
                    html.H4(closed_cases, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([

                    html.H3("Total Recovered", style={'font-size':'20px'}),
                    html.H4(total_recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Death", style={'font-size':'20px'}),
                    html.H4(total_death, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-2')
    ], className='row top-label'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Hr(className='hrtag'),
                    html.H3('Graphical Information of collected data around the world  :', className='h3-first'),
                    dcc.Dropdown(id='picker',options=options,value='All'),
                    dcc.Graph(id='scatter')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row first-graph'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Hr(className='hrtag'),
                    html.H3('Infected Vs Recovered :'),
                    dcc.Dropdown(id='pick',options=option,value='Infected'),
                    dcc.Graph(id='overview')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row second-graph'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Hr(className='hrtag'),
                    html.H3('World Map of Infection Covid-19 :'),
                    dcc.Graph(figure=fig2)
                ],className='card-body')
            ],className='card')
        ],className='col-lg-12')
    ],className='row third-graph'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Hr(className='hrtag'),
                    html.H3('United States Map of Infection Covid-19 :'),
                    dcc.Graph(figure=fig)
                ],className='card-body')
            ],className='card')
        ],className='col-lg-12')
    ],className='row forth-graph'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Confirmed Cases :-'),
                    dash_table.DataTable(id='table1',columns=[{"name": i, "id": i} for i in df11.columns],
                    data=df11.to_dict('records'),
                    style_table={"overflowY":"scroll",'height': 500},style_cell={'textAlign': 'center'},
                                         style_cell_conditional=[
                                             {
                                                 'if': {'column_id': 'Countries'},
                                                 'textAlign': 'right'
                                             }
                                         ]
                                         )
                ],className='card-body table-format')
            ],className='card')
        ],className='col-lg-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Recoved Cases :-'),
                    dash_table.DataTable(id='table2',columns=[{"name": j, "id": j} for j in df22.columns],
                    data=df22.to_dict('records'),style_table={"overflowY": "scroll",'height': 500},style_cell={'textAlign': 'center'},
                                         style_cell_conditional=[
                                             {
                                                 'if': {'column_id': 'Countries'},
                                                 'textAlign': 'right'
                                             }
                                         ])
                ],className='card-body table-format')
            ],className='card')
        ],className='col-lg-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Death cases :-'),
                    dash_table.DataTable(id='table3',columns=[{"name": k, "id": k} for k in df33.columns],
                    data=df33.to_dict('records'),style_table={"overflowY": "scroll",'height': 500},style_cell={'textAlign': 'center'},
                                         style_cell_conditional=[
                                             {
                                                 'if': {'column_id': 'Countries'},
                                                 'textAlign': 'right'
                                             }
                                         ])
                ],className='card-body table-format')
            ],className='card')
        ],className='col-lg-4')
    ],className='row'),
    html.Footer([
        html.Div(['© Copyright 2020 : ',
            html.A('Tuhin Mukherjee',href="https://whitexgod.github.io/cv/")
        ],className='footer-copyright text-center py-3',style={'color':'#fc172e'})
    ],className='page-footer font-small blue')
],className='container')


@app2.callback(Output('scatter','figure'), [Input('picker','value')])
def update_graph(type):

    if type=='All':

            pscat=covid_19_data.groupby('Last Update')['Confirmed'].sum().sort_values().reset_index()
            return {'data':[go.Scatter(x=pscat['Last Update'], y=pscat['Confirmed'], mode='markers', marker={'color':'#00a65a', 'size':8})],
               'layout':go.Layout(title='Line of Virus Spread per day', xaxis={'title':'By Date'}, yaxis={'title':'No. of cases'})}

    elif type=='total_confirmed':
            data1={'Countries': countries, 'Total cases' : total_c}
            df1=pd.DataFrame(data1)
            return {'data': [go.Bar(x=df1['Countries'], y=df1['Total cases'])],
               'layout': go.Layout(title='Total number of Confirmed cases across the world', xaxis={'title': 'Countries'}, yaxis = {'title': 'Number of Cases'})}

    elif type=='total_recovered':
            data2={'Countries': countries, 'Total cases' : total_r}
            df2=pd.DataFrame(data2)
            return {'data': [go.Bar(x=df2['Countries'], y=df2['Total cases'])],
               'layout': go.Layout(title='Total number of Recovered cases across the world',xaxis={'title': 'Countries'}, yaxis = {'title': 'Number of Cases'})}

    elif type=='total_death':
            data3={'Countries': countries, 'Total cases' : total_d}
            df3=pd.DataFrame(data3)
            return {'data': [go.Bar(x=df3['Countries'], y=df3['Total cases'])],
               'layout': go.Layout(title='Total number of Deaths cases across the world',xaxis={'title': 'Countries'}, yaxis = {'title': 'Number of Cases'})}


@app2.callback(Output('overview','figure'), [Input('pick','value')])
def update_graph(type):

    if type=='Infected':

        data4 = {'Countries': countries, 'Total cases': total_c}
        df4 = pd.DataFrame(data4)
        return {'data': [go.Pie(labels=df4['Countries'], values=df4['Total cases'])]}

    elif type=='total_recovered':

        data5 = {'Countries': countries, 'Total cases': total_r}
        df5 = pd.DataFrame(data5)
        return {'data': [go.Pie(labels=df5['Countries'], values=df5['Total cases'])]}



if __name__=="__main__":
   app2.run_server(debug=True)