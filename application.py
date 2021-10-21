import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import plotly.express as px

#---------------------------------------------------------------------------------------------

app = dash.Dash(__name__)

#---------------------------------------------------------------------------------------------

def clean_data(data, state_data):
    name_data = state_data.drop('Abbrev', axis = 1)

    data = data.loc[:, ~data.columns.str.contains('Total')]
    data = data.rename({'Unnamed: 1': 'Total'}, axis = 1)

    state_data = data[~data.index.str.contains(r'(C\.|U\.|S\.|Institute|Seminary|School|Graduate|Center|Conservatory|Laboratory|All)')]
    state_data = state_data.merge(name_data, left_index= True, right_on='State', how='left')
    state_data = state_data.set_index('State')

    state_data['Total_Science'] = state_data.iloc[:, 1:15].sum(axis = 1)
    state_data['Total_Engineering'] = state_data.iloc[:, 15:24].sum(axis = 1)
    state_data['Non_Science_Eng'] = state_data['Total'] - state_data['Total_Science'] - state_data['Total_Engineering']
    
    science = list(state_data.columns[1:15])
    science.append('Code')
    science.append('Total_Science')
    data_science = state_data[science]
    data_science = data_science.rename({'Total_Science':'Total'}, axis = 1)

    eng = list(state_data.columns[15:25])
    eng.append('Total_Engineering')
    data_eng = state_data[eng]
    data_eng = data_eng.rename({'Total_Engineering':'Total'}, axis = 1)

    data_total = state_data[['Total_Science', 'Total_Engineering', 'Non_Science_Eng', 'Code', 'Total']]
    data_total = data_total.rename({'Total_Science':'Science',
                                    'Total_Engineering':'Engineering',
                                    'Non_Science_Eng':'Others'}, axis = 1)

    return data_science, data_eng, data_total

def get_state_data(field_name = 'total', state_name = 'CA'):
    if field_name == 'total':
        my_frame = data_total
    elif field_name == 'science':
        my_frame = data_science
    else:
        my_frame = data_eng
    
    my_state_frame = my_frame[my_frame['Code'] == state_name].transpose().iloc[:-2, :]
    my_state_frame = my_state_frame.reset_index()
    my_state_frame.columns = ['Field', 'Count']

    return my_state_frame
#---------------------------------------------------------------------------------------------

doc_data = pd.read_csv('sed17-sr-tab007.csv', header = 5, index_col = 0, thousands=',')
doc_data = doc_data.astype('int32')

state_name_data = pd.read_csv('state_name.csv')

data_science, data_eng, data_total = clean_data(doc_data, state_name_data)

science_fields = data_science.columns[:-2]
eng_fields = data_eng.columns[:-2]
total_fields = data_total.columns[:-2]

#---------------------------------------------------------------------------------------------

# create a choropleth geo map
fig_map = px.choropleth(data_frame = data_science,
                        locations = 'Code',
                        color = 'Total',
                        color_continuous_scale = 'viridis',
                        locationmode = "USA-states",
                        scope = 'usa',
                        labels = {'Total':'Count'},
                        height = 600
                      )
fig_map.update_geos(showsubunits=False, showcoastlines = False)

CA_total_frame = get_state_data()
fig_pie = px.bar(data_frame = CA_total_frame,
                 y = 'Count',
                 x = 'Field',
                 text = 'Count',
                 color = 'Field',
                 labels = {'Field':'Sub-Fields'},
                 height = 600)
fig_pie.update_traces(textposition='outside')
fig_pie.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'showlegend': False})
#---------------------------------------------------------------------------------------------
# define dashboard layout
app.layout = html.Div(children = [
    html.H1(children='Science and Engineering PhDs Awarded in the US in 2017',
            style = {'font-family':'Helvetica',
                     'font-size': '50px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center'}
                     ),

    html.Div(children = [
        html.Div('Select a Field: ',
                 style = {'font-family':'Helvetica',
                          'font-size': '20px',
                          'textAlign': 'right',
                          'width':'35%',
                          'display': 'inline-block'
                          }),
        html.Div('',
                 style = {'font-family':'Helvetica',
                          'font-size': '20px',
                          'textAlign': 'right',
                          'width':'5%',
                          'display': 'inline-block'
                          }),
        dcc.RadioItems(
            id = 'display_scope',
            options=[
                {'label': 'Total', 'value': 'total'},
                {'label': 'Science Only', 'value': 'science'},
                {'label': 'Engineering Only', 'value': 'engineering'}
                ],
            value='total',
            labelStyle = {'display': 'inline-block', 'cursor': 'pointer', 'margin-right': '30px'},
            style = {'font-family':'Helvetica',
                     'font-size': '20px',
                     'width':'60%',
                     'textAlign': 'left',
                     'display': 'inline-block'})
    ]),

    html.Div(children = [
        dcc.Graph(
            id = 'world_map',
            figure = fig_map,
            hoverData = {'points': [{'location': 'CA'}]},
            style = {'width':'100%',
                    'display': 'inline-block',
                    'vertical-align': 'middle',
                    'align': 'left'})
    ]),

    html.Div(children='Detailed Distribution of Sub-Fields for Selected Field and State',
            style = {'font-family':'Helvetica',
                     'font-size': '20px',
                     'width':'100%',
                     'display': 'inline-block',
                     'textAlign': 'center'}
                     ),

    html.Div(children = [
        dcc.Graph(
            id = 'pie_chart',
            figure = fig_pie,
            style = {'width':'100%',
                    'display': 'inline-block',
                    'vertical-align': 'middle',
                    'align': 'left'})
    ]) 
])

#---------------------------------------------------------------------------------------------

# callback for updating datepicker component based on include_forecast radioitem
@app.callback(
    Output(component_id = 'world_map', component_property = 'figure'),
    Input(component_id = 'display_scope', component_property = 'value')
)
def update_world_map(radioitem_value):
    if radioitem_value == 'total':
        my_frame = data_total
    elif radioitem_value == 'science':
        my_frame = data_science
    else:
        my_frame = data_eng
    
    fig = px.choropleth(data_frame = my_frame,
                        locations = 'Code',
                        color = 'Total',
                        color_continuous_scale = 'viridis',
                        locationmode = "USA-states",
                        scope = 'usa',
                        labels = {'Total':'Count'},
                        height = 600,

                      )
    fig.update_geos(showsubunits=False, showcoastlines = False)
    return fig
        

# # callback for updating graph component based on selected country on map,
# # include_forecast radioitem, and date range on datepicker
@app.callback(
    Output(component_id = 'pie_chart', component_property = 'figure'),
    [Input(component_id = 'world_map', component_property = 'hoverData'),
     Input(component_id = 'display_scope', component_property = 'value')]
)
def update_trend(map_value, radioitem_value):
    # get country name from hoverData
    state = map_value['points'][0]['location']
    my_frame = get_state_data(field_name = radioitem_value, state_name=state)

    fig = px.bar(data_frame = my_frame,
                 y = 'Count',
                 x = 'Field',
                 text = 'Count',
                 color = 'Field',
                 labels = {'Field':'Sub-Fields'},
                 height = 600)
    fig.update_traces(textposition='outside')
    fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'showlegend': False})
    
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
