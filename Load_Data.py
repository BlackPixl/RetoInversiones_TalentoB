import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
db_user = 'admin'
db_password = 'admin'
db_host = 'localhost'  # or your database host
db_port = '5432'       # default PostgreSQL port
db_name = 'inversiones'

# Create a database connection
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Function to load a CSV file into a PostgreSQL table
def load_csv_to_db(csv_file, table_name):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists='append', index=False)

# Load CSV files into respective tables
#load_csv_to_db('./Data/catalogo_activos.csv', 'catalogo_activos')
#load_csv_to_db('./Data/catalogo_banca.csv', 'catalogo_banca')
#load_csv_to_db('./Data/cat_perfil_riesgo.csv', 'cat_perfil_riesgo')
load_csv_to_db('./Data/historico_aba_macroactivos.csv', 'staging_hist_aba_macroactivos')

print("Data loaded successfully!")
