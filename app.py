
# coding: utf-8

# In[223]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import time
import datetime


# In[224]:


#generate table
def generate_table(dataframe, max_rows=25):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# In[225]:


#read csv
data=pd.read_csv('data_explorimmo_27janvier.csv', ',')


# In[226]:


data['€']=(data['Loyer estimé'])-(data['prix_annonce']-30000)/(12*15)


# In[227]:


col=['Unnamed: 0','m2']
data.drop(col, axis=1, inplace=True)
data.columns=['Arrondissement', 'Prix', 'Publication','#Pièces', '#Chambres', 'Lien', 'Description', 'm2', 'Étage', 'Loyer estimé','Prix/m2', '€']
cols = data.columns.tolist()
cols = ['Arrondissement', 'm2', '#Pièces', '#Chambres', 'Étage', 'Prix', 'Prix/m2', 'Loyer estimé', '€', 'Description', 'Lien', 'Publication']
data = data[cols]


# In[228]:


data.sort_values('€', ascending=False, inplace=True)


# In[229]:


data


# In[246]:


#dash layout
app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
available_indicators = list(data)[:-3]
available_geo = data['Arrondissement'].unique()

app.layout = html.Div([
    
    html.H1(children='Apparts Paris',style={'text-align':'center','font-family':'monospace'}),
    #FIRST GRAPH
    html.Div([
        
        html.H2(children='Données de http://www.explorimmo.com ('+str(data.shape[0])+' annonces)',style={'text-align':'center','font-family':'monospace', 'margin-top':'5%'}),
        
        html.Div([
                html.Label('Choix arrondissement(s):'),
                dcc.Dropdown(
                    id='local-choice',
                    options=[
                        {'label': '1er', 'value': 1},
                        {'label': u'2ème', 'value': 2},
                        {'label': u'3ème', 'value': 3},
                        {'label': u'4ème', 'value': 4},
                        {'label': u'5ème', 'value': 5},
                        {'label': u'6ème', 'value': 6},
                        {'label': u'7ème', 'value': 7},
                        {'label': u'8ème', 'value': 8},
                        {'label': u'9ème', 'value': 9},
                        {'label': u'10ème', 'value': 10},
                        {'label': u'11ème', 'value': 11},
                        {'label': u'12ème', 'value': 12},
                        {'label': u'13ème', 'value': 13},
                        {'label': u'14ème', 'value': 14},
                        {'label': u'15ème', 'value': 15},
                        {'label': u'16ème', 'value': 16},
                        {'label': u'17ème', 'value': 17},
                        {'label': u'18ème', 'value': 18},
                        {'label': u'19ème', 'value': 19},
                        {'label': u'20ème', 'value': 20},
                    ],
                    multi=True,
                    value=list(range(1,21))
                ),
            ],style={'margin-bottom':'3%'}),
        
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='m2'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Prix'
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),
    ]),
    
    #SECOND GRAPH
    html.Div([
        html.Div([
            
            html.H2(children='Top 25',style={'margin':'3%','text-align':'center','font-family':'monospace'}),
            
            html.Div([
                dcc.Dropdown(
                    id='choice-feature',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='€'
                ),
            ],
            style={'width': '95%'}),
            
            dcc.Graph(id='indicator-graphic2'),
            
            html.H2(children='Détails classement:',style={'margin':'3%' ,'text-align':'center','font-family':'monospace'}),
            
            html.Table(id='table_top50', style={'border':'1px'})

        ])
    ])
    #END SECOND
])


# In[247]:


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
    dash.dependencies.Input('local-choice', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name, local_choice):
    dfff = None
    dfff = data.copy()
    dfff = dfff.iloc[0:0]
    for i in range(len(local_choice)):
        dfff = dfff.append(data[data['Arrondissement'] == int(local_choice[i])])
    dfff = dfff[dfff['m2'] > 9]
    
    return {
        'data': [go.Scatter(
            x=dfff[xaxis_column_name],
            y=dfff[yaxis_column_name],
            text=dfff['Description'] + ' ' + dfff['Lien'],
            mode='markers',
            marker={
                'size': 10,
                'color':dfff['Arrondissement'],
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
                'colorscale':'Jet',
                'showscale' : True,
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#CALLBACK TOP50 GRAPH
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('local-choice', 'value'),
    dash.dependencies.Input('choice-feature', 'value')])
def update_graph(local_choice, choice_feature):
    dfff = None
    dfff = data.copy()
    dfff = dfff.iloc[0:0]
    for i in range(len(local_choice)):
        dfff = dfff.append(data[data['Arrondissement'] == int(local_choice[i])])

    dfff = dfff.sort_values(choice_feature, ascending=False)
    dfff = dfff[dfff['m2'] > 9]
    dfff.reset_index(inplace=True)
    print(dfff.shape[0])
    dfff = dfff[:25]
    
    return {
        'data': [go.Bar(
            x=dfff.index,
            y=dfff[choice_feature],
            text=dfff['Description'] + ' ' + dfff['Lien'],
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'classement',
            },
            yaxis={
                'title': choice_feature,
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#CALLBACK TABLE_TOP50
@app.callback(
    dash.dependencies.Output('table_top50', 'children'),
    [dash.dependencies.Input('local-choice', 'value'),
    dash.dependencies.Input('choice-feature', 'value')])
def update_table(local_choice, choice_feature):
    dfff = None
    dfff = data.copy()
    dfff = dfff.iloc[0:0]
    for i in range(len(local_choice)):
        dfff = dfff.append(data[data['Arrondissement'] == int(local_choice[i])])

    dfff = dfff.sort_values(choice_feature, ascending=False)
    dfff = dfff[dfff['m2'] > 9]
    dfff.reset_index(inplace=True)
    dfff = dfff[:25]
    dfff['Rang'] = dfff.index
    cols = dfff.columns.tolist()
    cols = cols[-1:]+cols[:-1]
    dfff = dfff[cols]
    dfff.drop('Description', axis=1, inplace=True)

    
    dfff.drop('index', axis=1, inplace=True)
    
    return generate_table(dfff)
    
    
if __name__ == '__main__':
    app.run_server()

