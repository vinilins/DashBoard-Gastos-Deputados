import pandas as pd
import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

df_2016 = pd.read_csv('csvs/2016.csv')
df_2017 = pd.read_csv('csvs/2017.csv')
df_2018 = pd.read_csv('csvs/2018.csv')
df_2019 = pd.read_csv('csvs/2019.csv')

css_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=css_style)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

site = {
    'background': '#F4EFE5',
    'width': '1366px',
    'height': '1000px',
    'margin-top': 0,
    'margin-left': 'auto',
    'margin-bottom': 0,
    'margin-right': 'auto',
    'border': '1px solid black',
    'padding': '20px'
}

header = {
    'background': '#A5AAAB',
    'margin-left': '-18px',
    'margin-top': '-36px',
    'width': '1402px',
    'height': '100px',
}

conteudo = {
    'background': '#F4EFE5',
    'width': '1336px',
    'height': '500px',
}

footer = {
    'width': '1000px',
    'height': '100px',
}

conteudoleft = {
    'width': '668px',
    'height': '400px',
    'float': 'left',
}

conteudoright = {
    'width': '668px',
    'height': '300px',
    'float': 'right',
}

conteudomeio = {
    'width': '668px',
    'height': '30px',
}

h2 = {
    'margin-left': '8px',
    'text-shadow': '2px 2px 8px gray',
}

h5 = {
    'font-style': 'italic',
    'text-align': 'center',
    'text-decoration': 'underline'
}

app.layout = html.Div(id='site', children=[

    html.Div(id='header', children=[

        html.H2(children='GASTOS DOS DEPUTADOS BRASILEIROS', style=h2), html.H5(children='DashBoard dos Gastos dos Deputados e Partidos Brasileiros de 2016 à 2019', style=h5)], style=header),
    html.Div(id='conteudo', children=[

        html.Div(id='conteudo-left', children=[
            html.Label(children='Selecione o Ano', style={'margin-top': '20px', 'font-size': '17px', 'font-weight': 'bold'}),
            dcc.RadioItems(
                id='radio-box',
                options=[{'label': str(i), 'value': str(i)} for i in range(2016,2020)],
                value='2019'
            ),
            html.Label(children='Selecione o Partido', style={'font-size': '17px', 'font-weight': 'bold'}),
            dcc.Dropdown(id='dropdown-1'),
            html.Label(children='Selecione o Parlamentar', style={'font-size': '17px', 'font-weight': 'bold'}),
            dcc.Dropdown(id='dropdown-2'),
            html.Label(children='Comparar Gastos', style={'font-size': '17px', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='comparacao',
                multi=True
            ),
            html.Br(),
            html.H5(children='Gastos 2016 à 2019:', style={'font-weight': 'bold'}),
            html.H6(id='gastos', children=[]),
            html.H6(id='gastos1', children=[]),
            html.H6(id='gastos2', children=[]),
            html.Br(),
            html.Img(id='gastos3', src='', style={'width': '200px', 'height': '80px', 'margin-left': '100px', 'margin-top': '-18px'})
        ], style=conteudoleft),

         html.Label(id='conteudo-right', children=[
             dcc.Graph(
                id='graph',
                figure={
                    'layout': {
                        'title': 'Gastos',
                    }
                },
                style={'margin-left': '30px', 'margin-top': '20px'},
             ),
             dcc.Graph(
                id='graph-2',
                figure={

                    'data': [
                        {'x': '1', 'y':'1', 'type': 'bar', 'name': 'd'}

                    ],
                    'layout': {
                        "height": 250,
                        'title': 'Comparação de Gastos'
                    }
                },
                style={'margin-left': '30px'}
            )
                                ], style=conteudoright),
    ], style=conteudo),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(id='output5'),
    html.Div(id='rodape', children=[html.Label(id='texto2', children=[html.Label(id='output2'),
                                                                      html.Label(id='output4'),
                                                                      ]),
                                    ], style=footer)], style=site)

def tratarString(string):
    cont=0
    cont2=0
    controle=0
    string = str(string)
    lista = []
    for i in range(len(string)-1,-1,-1):
      if controle==0:
        cont2+=1
        if string[i]=='.':
          lista.append(',')
          controle = 1
          continue
        lista.append(string[i])
      if controle==1:
        cont+=1
        lista.append(string[i])
        if cont%3==0 and i!=0:
          lista.append(".")
    cont2-=1
    if cont2>2:
      cont2 = cont2 - 2
      for i in range(0,cont2):
        lista.pop(0)
    elif cont2<2:
        if cont2==1:
            lista.insert(0,'0')
        elif cont2==0:
            lista.insert(0,'0')
            lista.insert(0,'0')
    string = ''.join(lista[::-1])
    return string

@app.callback(Output('gastos', 'children'),
              [Input('dropdown-1', 'value')])
def update_output(input1):
    somador2 = 0.00
    if input1==None:
        input1 = 'Partidos'
        for i in range(len(df_2016)):
                somador2+=float(df_2016.loc[i].valorLiquido)
        for i in range(len(df_2017)):
                somador2+=float(df_2017.loc[i].valorLiquido)
        for i in range(len(df_2018)):
                somador2+=float(df_2018.loc[i].valorLiquido)
        for i in range(len(df_2019)):
                somador2+=float(df_2019.loc[i].valorLiquido)
        return 'Gastos Totais do(s) {}: R$ {}'.format(input1, tratarString(somador2))
    else:
        for i in range(len(df_2016)):
            if df_2016.loc[i].siglaPartido == input1:
                somador2+=float(df_2016.loc[i].valorLiquido)
        for i in range(len(df_2017)):
            if df_2017.loc[i].siglaPartido == input1:
                somador2+=float(df_2017.loc[i].valorLiquido)
        for i in range(len(df_2018)):
            if df_2018.loc[i].siglaPartido == input1:
                somador2+=float(df_2018.loc[i].valorLiquido)
        for i in range(len(df_2019)):
            if df_2019.loc[i].siglaPartido == input1:
                somador2+=float(df_2019.loc[i].valorLiquido)
    return 'Gastos Totais do(s) {}: R${}'.format(input1, tratarString(somador2))

@app.callback(Output('gastos1', 'children'),
              [Input('dropdown-2', 'value')])
def update_output(input2):
    somador2 = 0.00
    if input2==None:
        input2 = 'Deputado'
    else:
        for i in range(len(df_2016)):
            if df_2016.loc[i].nomeParlamentar == input2:
                somador2+=float(df_2016.loc[i].valorLiquido)
        for i in range(len(df_2017)):
            if df_2017.loc[i].nomeParlamentar == input2:
                somador2+=float(df_2017.loc[i].valorLiquido)
        for i in range(len(df_2018)):
            if df_2018.loc[i].nomeParlamentar == input2:
                somador2+=float(df_2018.loc[i].valorLiquido)
        for i in range(len(df_2019)):
            if df_2019.loc[i].nomeParlamentar == input2:
                somador2+=float(df_2019.loc[i].valorLiquido)
    return 'Gastos Totais do(a) {}: R${}'.format(input2, tratarString(somador2))

@app.callback(Output('gastos2', 'children'),
              [Input('dropdown-2', 'value')])
def update_output(input2):
    estado = ''
    if input2==None:
        return 'Estado do Deputado Selecionado: ', estado
    for i in range(len(df_2016)):
        if df_2016.loc[i].nomeParlamentar == input2:
            estado = df_2016.loc[i].siglaUF
            return 'Estado do Deputado: ', estado
    for i in range(len(df_2017)):
        if df_2017.loc[i].nomeParlamentar == input2:
            estado = df_2017.loc[i].siglaUF
            return 'Estado do Deputado: ', estado
    for i in range(len(df_2018)):
        if df_2018.loc[i].nomeParlamentar == input2:
            estado = df_2018.loc[i].siglaUF
            return 'Estado do Deputado: ', estado
    for i in range(len(df_2019)):
        if df_2019.loc[i].nomeParlamentar == input2:
            estado = df_2019.loc[i].siglaUF
            return 'Estado do Deputado: ', estado
    return 'Estado do Deputado: ', estado


def selecionar_dataframe(ano):
    if ano == '2016':
        global df_2016
        return df_2016
    elif ano == '2017':
        global df_2017
        return df_2017
    elif ano == '2018':
        global df_2018
        return df_2018
    else:
        global df_2019
        return df_2019

@app.callback(Output('dropdown-2', 'options'),
              [Input('dropdown-1', 'value'),
               Input('radio-box', 'value')])
def update_output2(input, input2):
    new_df = selecionar_dataframe(input2)
    l2=[]
    t = new_df.nomeParlamentar.size
    for i in range(t):
        if new_df.loc[i].siglaPartido == input:
            l2.append(new_df.loc[i].nomeParlamentar)
    return [{'label': str(i), 'value': str(i)} for i in l2]


def gastos_parlamentar_ano(nome):
    ano,valores=[],[]
    t = df_2016.nomeParlamentar.size
    for i in range(t):
        if df_2016.loc[i].nomeParlamentar == nome:
            ano.append('2016')
            valores.append(df_2016.loc[i].valorLiquido)
            break
    t = df_2017.nomeParlamentar.size
    for i in range(t):
        if df_2017.loc[i].nomeParlamentar == nome:
            ano.append('2017')
            valores.append(df_2017.loc[i].valorLiquido)
            break
    t = df_2018.nomeParlamentar.size
    for i in range(t):
        if df_2018.loc[i].nomeParlamentar == nome:
            ano.append('2018')
            valores.append(df_2018.loc[i].valorLiquido)
            break
    t = df_2019.nomeParlamentar.size
    for i in range(t):
        if df_2019.loc[i].nomeParlamentar == nome:
            ano.append('2019')
            valores.append(df_2019.loc[i].valorLiquido)
            break
    return ano,valores



@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown-2', 'value'),
     Input('radio-box', "value")])
def update_output(value, input2):
    X,Y = gastos_parlamentar_ano(value)
    l2=[]
    new_df = selecionar_dataframe(input2)
    t = new_df.nomeParlamentar.size
    for i in range(t):
        if new_df.loc[i].nomeParlamentar == input:
            l2.append(new_df.loc[i].valorLiquido)
    if str(value) == "None":
        value = "Parlamentar"
    return {
        'data': [{'y': Y, 'x': X, 'marker': {'color': 'black'}}],
        'layout': {
            "height": 250,
            'title': 'Gastos de '+str(value),
            "xaxis": {
                "title": {"text": 'Ano(s)'}
            },
            "yaxis": {
                "title": {"text": 'R$'}
            }
        }
    }


def valores_partido(new_df):
    valor,partido=[],[]
    t = new_df.nomeParlamentar.size
    for i in range(t):
        if new_df.loc[i].siglaPartido not in partido:
            partido.append(new_df.loc[i].siglaPartido)
            valor.append(float(new_df.loc[i].valorLiquido))
        else:
            ind = partido.index(new_df.loc[i].siglaPartido)
            valor[ind] += float(new_df.loc[ind].valorLiquido)
    return valor,partido

@app.callback(
    Output('output5', "children"),
    [Input('radio-box', "value")])
def update_graphs(input):
    new_df = selecionar_dataframe(input)
    X,Y =  valores_partido(new_df)
    return [
        dcc.Graph(
            id='column',
            figure={
                "data": [
                    {
                        "x": Y,
                        "y": X,
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    'title' : 'Gastos dos partidos em '+input,
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": 'R$'}
                    },
                    "height": 270,
                    "margin": {"t": 35, "l": 20, "r": 20},
                },
            },
        )
    ]

@app.callback(
    Output('dropdown-1', 'options'),
    [Input('radio-box', "value")])
def update_graphs(input):
    partidos = ['AVANTE', 'PSDB', 'MDB', 'DEM', 'PP', 'PSC', 'PDT', 'PODE', 'PSB', 'PT', 'PRB', 'PTB', 'CIDADANIA', 'PSOL', 'PV', 'SOLIDARIEDADE', 'PSD', 'PCdoB', 'PR', 'PL', 'PSL', 'PROS', 'REDE', 'PATRI', 'NOVO', 'PPS', 'PHS', 'PRP', 'S.PART.', 'PMN']
    return [{'label': str(i), 'value': str(i)} for i in partidos]



def valor(lista_nomes, df):
    if lista_nomes != []:
        valores=[]
        t = df.nomeParlamentar.size
        for nome in lista_nomes:
            for i2 in range(t):
                if df.loc[i2].nomeParlamentar == nome:
                    valores.append(df.loc[i2].valorLiquido)
        return valores


@app.callback(
    Output('graph-2', 'figure'),
    [Input('radio-box', 'value'),
     Input('comparacao', "value")])
def update_graphs(input, input2):
    if str(input2) != "None":
        new_df = selecionar_dataframe(input)
        lista_valores = valor(input2, new_df)
        return {
                    'data': [
                        {'x': input2, 'y': lista_valores, 'type': 'bar', 'marker': {'color': 'gray'}}

                    ],
                    'layout': {
                        "height": 270,
                        'title': 'Comparação de Gastos em '+input,
                        "yaxis": {
                            "title": {"text": 'R$'}
                        },
                    }
                }
    else:
        return {
                    'data': [
                        {'x': 0, 'y': 0, 'type': 'bar', 'name': 'd'}

                    ],
                    'layout': {
                        "height": 270,
                        'title': 'Comparação de Gastos',
                        "yaxis": {
                            "title": {"text": 'R$'}
                        },
                    }
                }

@app.callback(
    Output('comparacao', 'options'),
    [Input('radio-box', 'value')])
def update_graphs(input):
    nomes=[]
    new_df = selecionar_dataframe(input)
    t = new_df.nomeParlamentar.size
    for i in range(t):
        nomes.append(new_df.loc[i].nomeParlamentar)
    return [{'label': str(i), 'value': str(i)} for i in nomes]

@app.callback(
    dash.dependencies.Output('gastos3', 'src'),
    [Input('gastos2', 'children')])
def update_image_src(image_path):
    if str(image_path[1]) == '':
        image_path = 'estados/None.png'
    else:
        image_path = 'estados/'+image_path[1]+'.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

if __name__ == '__main__':
    app.run_server(debug=True)
