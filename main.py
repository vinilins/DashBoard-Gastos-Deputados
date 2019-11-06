import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import base64
import random
import webcolors as wc
from dash.dependencies import Input, Output
from libs import functions as fnt


global df_2016
global df_2017
global df_2018
global df_2019

df_2016 = fnt.selecionar_dataframe(2016)
df_2017 = fnt.selecionar_dataframe(2017)
df_2018 = fnt.selecionar_dataframe(2018)
df_2019 = fnt.selecionar_dataframe(2019)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([html.Div([html.Label(children="Menu de Opções", id="texto-menu")], className="cimalateralesquerda"),
            html.Div([html.Label(children='Selecione o Ano', id="anos"),
                    dcc.RadioItems(
                    id="radio-box",
                        options=[{'label': '2016', 'value': '2016'}, {'label': '2017', 'value': '2017'},
                                {'label': '2018', 'value': '2018'}, {'label': '2019', 'value': '2019'}],
                        value='2016',
                        labelClassName="text-radio-box"
                    ),
                    html.Label(children='Selecione o partido', id="partido"),
                    dcc.Dropdown(id='dropdown-partido', placeholder="Selecione um partido"),
                    html.Label(children='Selecione o Parlamentar', id="parlamentar"),
                    dcc.Dropdown(id='dropdown-parlamentar', placeholder="Selecione um parlamentar"),
                    html.Label(children='Comparar Gastos', id="gastos"),
                    dcc.Dropdown(id='dropdown-comparacao', placeholder="Selecione outro parlamentar", multi=True, 
                                loading_state= {})], 
                    className="baixolateralesquerda")], 
            className="lateralesquerda"),
    html.Div([  html.Div([html.Label(children="Gastos dos Deputados brasileiros", id="texto-titulo")], className="superior"),
                html.Div([
                    html.Div(children=[], className="divisoesmenores2", id="output4"),
                    html.Div([html.Label(id="estado", children=""), html.Img(id="imagemestado", src='')], className="divisoesmenores3"),
                     html.Div(children=[], className="divisoesmenores3", id="gastosdeputado"),
                     html.Div([], className="divisoesmenores1", id="gastospartido"),
                     html.Div(children=[], className="divisoesmenores4", id='output5')
                ], className="divdasdivisoesmenores")], 
                className="lateraldireita"),
    ], className="principal")



@app.callback(Output('estado', 'children'),
              [Input('dropdown-parlamentar', 'value')])
def update_output(input2):
    estado = ''
    if input2==None:
        return 'Estado do Deputado: ', estado
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



@app.callback(Output('imagemestado', 'src'),
            [Input('estado', 'children')])
def update_image_src(image_path):
    if str(image_path[1]) == '':
        image_path = 'estados/None.png'
    else:
        image_path = 'estados/'+image_path[1]+'.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())



@app.callback(Output('dropdown-parlamentar', 'options'),
              [Input('dropdown-partido', 'value'),
               Input('radio-box', 'value')])
def update_output2(input, input2):
    l2 = []
    for i in range(len(df_2016)):
        if df_2016.loc[i].siglaPartido == input:
            l2.append(df_2016.loc[i].nomeParlamentar)
    for i in range(len(df_2017)):
        if df_2017.loc[i].siglaPartido == input:
            l2.append(df_2017.loc[i].nomeParlamentar)
    for i in range(len(df_2018)):
        if df_2018.loc[i].siglaPartido == input:
            l2.append(df_2018.loc[i].nomeParlamentar)
    for i in range(len(df_2019)):
        if df_2019.loc[i].siglaPartido == input:
            l2.append(df_2019.loc[i].nomeParlamentar)
    return [{'label': str(i), 'value': str(i)} for i in l2]



@app.callback(
    Output('output5', "children"),
    [Input('radio-box', "value")])
def update_graphs(input):
    new_df = fnt.selecionar_dataframe(input)
    X,Y =  fnt.valores_partido(new_df)
    cores = []
    for i in range(len(Y)):
        x,y,z = random.randint(0,256),random.randint(0,256),random.randint(0,256)
        cor = (x,y,z)
        cores.append(wc.rgb_to_hex(cor))

    return [
        dcc.Graph(
            id='column',
            figure={
                "data": [{  "x": Y,
                            "y": X,
                            "type": "bar",
                            "width": 1,
                            "text": [str(e) for e in Y],
                            "textposition": "inside",
                            "marker": {"color": cores}
                            },
                        ],
                "layout": {
                    'title' : {"text": 'Gastos dos Partidos em '+input, "y": 0.95, "x": 0.45},
                    "legend": {},
                    "xaxis": {"automargin": True},
                    "yaxis": {"automargin": True, "title": {"text": 'R$'}},
                    "colorbar":  '#111111', 
                    "font": {"color": "#111111", "family": "roboto"},
                    "margin": {"l": 50 ,"t": 30},
                    "height": 230,
                    "width": 1130
                    }},
                style={})]
#y: 0.75
#"height": "115%", "margin-top": -25

@app.callback(
    dash.dependencies.Output('output4', 'children'),
    [dash.dependencies.Input('dropdown-parlamentar', 'value'),
     Input('radio-box', "value")])
def update_output(value, input2):
    X,Y = fnt.gastos_parlamentar_ano(value)
    l2=[]
    new_df = fnt.selecionar_dataframe(input2)
    t = new_df.nomeParlamentar.size
    for i in range(t):
        if new_df.loc[i].nomeParlamentar == input:
            l2.append(new_df.loc[i].valorLiquido)
    if str(value) == "None":
        value = "Parlamentar"
    return [
        dcc.Graph(id='graph',
                figure={'data': [{'y': Y, 'x': X, 'marker': {'color': '#111111'}}],
                    'layout': {
                        'title': 'Gastos de '+str(value),
                        "xaxis": {
                            "automargin": True,
                            "title": {"text": 'Ano(s)'}},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": 'R$'}}
                        }},
                style={"height": "99%", "width": "100%"}
                )]


@app.callback(Output('gastospartido', 'children'),
              [Input('dropdown-partido', 'value')])
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
        return 'Gastos Totais dos {} (2016 à 2019): R$ {}'.format(input1, fnt.tratarString(somador2))
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
    return 'Gastos Totais do {} (2016 à 2019): R${}'.format(input1, fnt.tratarString(somador2))


@app.callback(Output('gastosdeputado', 'children'),
              [Input('dropdown-parlamentar', 'value')])
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
    return 'Gastos Totais do(a) {}: R${}'.format(input2, fnt.tratarString(somador2))

@app.callback(
    Output('dropdown-partido', 'options'),
    [Input('radio-box', "value")])
def update_graphs(input):
    partidos = ['AVANTE', 'PSDB', 'MDB', 'DEM', 'PP', 'PSC', 'PDT', 'PODE', 'PSB', 'PT', 'PRB', 'PTB', 'CIDADANIA', 'PSOL', 'PV', 'SOLIDARIEDADE', 'PSD', 'PCdoB', 'PR', 'PL', 'PSL', 'PROS', 'REDE', 'PATRI', 'NOVO', 'PPS', 'PHS', 'PRP', 'S.PART.', 'PMN']
    return [{'label': str(i), 'value': str(i)} for i in partidos]

@app.callback(
    Output('dropdown-comparacao', 'options'),
    [Input('radio-box', 'value')])
def update_graphs(input):
    nomes=[]
    new_df = fnt.selecionar_dataframe(input)
    t = new_df.nomeParlamentar.size
    for i in range(t):
        nomes.append(new_df.loc[i].nomeParlamentar)
    return [{'label': str(i), 'value': str(i)} for i in nomes]


if __name__ == '__main__':
    app.run_server(debug=True)