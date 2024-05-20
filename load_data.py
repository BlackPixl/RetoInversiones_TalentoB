import pandas as pd
import logging
from sqlalchemy import create_engine

log_file_path = 'logs/data_loading.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_user = 'admin'
db_password = 'admin'
db_host = 'localhost'
db_port = '5432'
db_name = 'inversiones'

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
