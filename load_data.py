import pandas as pd
import logging
import psycopg2
from sqlalchemy import create_engine

log_file_path = 'logs/data_loading.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_user = 'admin'
db_password = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'inversiones'

connection_params = {
    'user' : db_user,
    'password' : db_password,
    'host' : db_host,
    'port' : db_port,
    'dbname' : db_name
}

# creación de tablas (en caso de que no existan)
sql_file_path = 'sql_scripts/create_tables.sql'

with open(sql_file_path, 'r') as file:
    sql_script = file.read()

logging.info("Started script for table creation")
try:
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()
    cursor.execute(sql_script)
    connection.commit()
    logging.info("Execution successful")
except Exception as e:
    logging.error(f"Error executing script: {e}")
    connection.rollback()
finally:
    cursor.close()
    connection.close()
    logging.info("Ended script for table creation")

# cargue de datos.
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

def load_csv_to_db(csv_file, table_name):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists='append', index=False)

try:
    load_csv_to_db('./origin_data/catalogo_activos.csv', 'catalogo_activos')
    load_csv_to_db('./origin_data/catalogo_banca.csv', 'catalogo_banca')
    load_csv_to_db('./origin_data/cat_perfil_riesgo.csv', 'cat_perfil_riesgo')
    load_csv_to_db('./origin_data/historico_aba_macroactivos.csv', 'staging_hist_aba_macroactivos')
    logging.info("Data loading successful")
except Exception as e:
    logging.error(f"Error executing script: {e}")
finally:
    logging.info("Ended script for data loading")
