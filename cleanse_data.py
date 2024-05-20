import psycopg2
import logging

connection_params = {
'user' : 'admin',
'password' : 'admin',
'host' : 'localhost',
'port' : '5432',
'dbname' : 'inversiones'
}

log_file_path = 'logs/data_cleaning.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

sql_file_path = 'sql_scripts/cleanse_data.sql'

with open(sql_file_path, 'r') as file:
    sql_script = file.read()

logging.info("Started script for data cleaning")
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
    logging.info("Ended script for data cleaning")
