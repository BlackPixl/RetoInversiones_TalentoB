import pandas as pd
import psycopg2
import dash
import plotly.express as px
from sqlalchemy import create_engine
from dash import dcc, html
from dash.dependencies import Input, Output

# Leer archivo con la sentencia sql.
query_file = 'GetData.sql'
with open(query_file, 'r') as file:
    sql_query = file.read()

# Parametros de conección con la base de datos.
db_user = 'admin'
db_password = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'inversiones'

# Conexión a la base de datos.
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Lectura de los datos desde la base de datos.
df = pd.read_sql_query(sql_query, engine)

# Preprocesar los datos
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        dcc.Dropdown(
            id='client-dropdown',
            options=[{'label': str(id), 'value': id} for id in df['id_sistema_cliente'].unique()],
            placeholder='Selecciona un cliente',
            style={'width': '50%', 'display':'inline-block'},
            searchable=True
            ),
        style={'text-align':'center'}
    ),
    html.Div([
        html.Div(dcc.Graph(id='portfolio-pie-chart'), style={'width':'50%', 'display':'inline-block'}),
        html.Div(dcc.Graph(id='portfolio-pie-chart-activos'), style={'width':'50%', 'display':'inline-block'})],
        style={'display': 'flex', 'justify-content': 'space-around'}
    ),
    html.Div([
        html.Div(dcc.Graph(id='portfolio-banca-pie-chart'),  style={'width':'50%', 'display':'inline-block'}),
        html.Div(dcc.Graph(id='risk-profile-pie-chart'),  style={'width':'50%', 'display':'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'space-around'}
    ),
    html.Div([
        html.Div(dcc.Graph(id='macroactivo-banca-bar-chart'),  style={'width':'50%', 'display':'inline-block'}),
        html.Div(dcc.Graph(id='macroactivo-riesgo-bar-chart'),  style={'width':'50%', 'display':'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'space-around'}),
    dcc.Graph(id='portfolio-line-chart'),
])

@app.callback(
    [Output('portfolio-pie-chart', 'figure'),
     Output('portfolio-pie-chart-activos', 'figure'),
     Output('portfolio-banca-pie-chart', 'figure'),
     Output('risk-profile-pie-chart', 'figure'),
     Output('portfolio-line-chart', 'figure'),
     Output('macroactivo-banca-bar-chart', 'figure'),
     Output('macroactivo-riesgo-bar-chart', 'figure')],  # Nueva gráfica
    [Input('client-dropdown', 'value')]
)
def update_graphs(selected_client):
    if not selected_client:
        # Si no hay cliente seleccionado, mostrar las gráficas con el total de los datos
        
        last_date = df['date'].max()
        last_date_df = df[df['date'] == last_date]

        # Gráfica de pastel para la última fecha disponible con todos los datos (macroactivo)
        
        pie_chart_macroactivos = px.pie(last_date_df, names='macroactivo', values='aba',
                           title=f'Distribución de macroactivos para {last_date.strftime("%Y-%m")}')
                           
        #Gráfica de pasteñ distribución activos
        pie_chart_activos = px.pie(last_date_df, names='activo', values='aba',
                           title=f'Distribución de activos para {last_date.strftime("%Y-%m")}')

        # Gráfica de pastel para la última fecha disponible con todos los datos (banca)
        banca_pie_chart = px.pie(last_date_df, names='banca', values='aba',
                                 title=f'Distribución del portafolio por banca para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de pastel para la última fecha disponible con todos los datos (perfil de riesgo)
        risk_pie_chart = px.pie(last_date_df, names='perfil_riesgo', values='aba',
                                title=f'Distribución del perfil de riesgo para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de líneas con el total de aba de todos los clientes
        total_df = df.groupby(['date', 'macroactivo'], as_index=False)['aba'].sum()
        line_chart = px.line(total_df, x='date', y='aba', color='macroactivo',
                             title='Evolución del total de aba de todos los clientes a través del tiempo')
        
        # Nueva gráfica de barras apiladas para la distribución de macroactivos por banca
        macroactivo_banca_df = last_date_df.groupby(['banca', 'macroactivo'], as_index=False)['aba'].sum()
        bar_chart_bank = px.bar(macroactivo_banca_df, x='banca', y='aba', color='macroactivo', 
                           title='Distribución de macroactivos por banca', barmode='stack')
                           
        # Nueva gráfica de barras apiladas para la dostrobucion de macroactivos por riesgo
        macroactivo_riesgo_df = last_date_df.groupby(['perfil_riesgo', 'macroactivo'], as_index=False)['aba'].sum()
        bar_chart_risk = px.bar(macroactivo_riesgo_df, x='perfil_riesgo', y='aba', color='macroactivo', 
                           title='Distribución de macroactivos por banca', barmode='stack')

    else:
        # Filtrar los datos para el cliente seleccionado
        client_df = df[df['id_sistema_cliente'] == selected_client]
        last_date = client_df['date'].max()
        last_date_df = client_df[client_df['date'] == last_date]

        # Gráfica de pastel para la última fecha disponible del cliente seleccionado (macroactivo)
        
        pie_chart_macroactivos = px.pie(last_date_df, names='macroactivo', values='aba',
                           title=f'Portafolio del cliente {selected_client} para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de pastel para la última fecha disponible del cliente seleccionado.
        pie_chart_activos = px.pie(last_date_df, names='activo', values='aba',
                           title=f'Distribución de activos para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de pastel para la última fecha disponible del cliente seleccionado (banca).
        banca_pie_chart = px.pie(last_date_df, names='banca', values='aba',
                                 title=f'Distribución del portafolio por banca del cliente {selected_client} para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de pastel para la última fecha disponible del cliente seleccionado (perfil de riesgo).
        risk_pie_chart = px.pie(last_date_df, names='perfil_riesgo', values='aba',
                                title=f'Distribución del perfil de riesgo del cliente {selected_client} para {last_date.strftime("%Y-%m")}')
        
        # Gráfica de líneas para la evolución del portafolio del cliente seleccionado.
        total_df = client_df.groupby(['date', 'macroactivo'], as_index=False)['aba'].sum()
        line_chart = px.line(total_df, x='date', y='aba', color='macroactivo',
                             title=f'Evolución del portafolio del cliente {selected_client} a través del tiempo')
        
        # Gráfica de barras apiladas para la distribución de macroactivos por banca.
        macroactivo_banca_df = last_date_df.groupby(['banca', 'macroactivo'], as_index=False)['aba'].sum()
        bar_chart_bank = px.bar(macroactivo_banca_df, x='banca', y='aba', color='macroactivo', 
                           title=f'Distribución de macroactivos por banca del cliente {selected_client}', barmode='stack')
        
        # Gráfica de barras apiladas para la distribución de macroactivos por riesgo.
        macroactivo_riesgo_df = last_date_df.groupby(['perfil_riesgo', 'macroactivo'], as_index=False)['aba'].sum()
        bar_chart_risk = px.bar(macroactivo_riesgo_df, x='perfil_riesgo', y='aba', color='macroactivo', 
                           title=f'Distribución de macroactivos por riesgo del cliente {selected_client}', barmode='stack')

    return pie_chart_macroactivos, pie_chart_activos, banca_pie_chart, risk_pie_chart, line_chart, bar_chart_bank, bar_chart_risk

if __name__ == '__main__':
    app.run_server(debug=True)