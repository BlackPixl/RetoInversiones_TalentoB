import pandas as pd
from sqlalchemy import create_engine

# Parámetros de conexión (normalmente se configuran como variables de entorno).
db_user = 'admin'
db_password = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'inversiones'

# Conexión con la base de datos.
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Load to csv carga 
def load_csv_to_db(csv_file, table_name):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists='append', index=False)

# Load CSV files into respective tables
load_csv_to_db('./Data/catalogo_activos.csv', 'catalogo_activos')
load_csv_to_db('./Data/catalogo_banca.csv', 'catalogo_banca')
load_csv_to_db('./Data/cat_perfil_riesgo.csv', 'cat_perfil_riesgo')
load_csv_to_db('./Data/historico_aba_macroactivos.csv', 'staging_hist_aba_macroactivos')

print("Data loaded successfully!")
