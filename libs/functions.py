import pandas as pd

df_2016 = pd.read_csv('C:/Users/vinny/Desktop/Projeto e Relatório - Estatística/refatoracaProjeto/csvs/2016.csv')
df_2017 = pd.read_csv('C:/Users/vinny/Desktop/Projeto e Relatório - Estatística/refatoracaProjeto/csvs/2017.csv')
df_2018 = pd.read_csv('C:/Users/vinny/Desktop/Projeto e Relatório - Estatística/refatoracaProjeto/csvs/2018.csv')
df_2019 = pd.read_csv('C:/Users/vinny/Desktop/Projeto e Relatório - Estatística/refatoracaProjeto/csvs/2019.csv')

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