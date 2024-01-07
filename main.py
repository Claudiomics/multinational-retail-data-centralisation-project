#from data_cleaning import DatabaseCleaning
from database_utils import DatabaseConnector
import yaml
from data_extraction import DataExtractor


''' This is the script where I will use the three different classes (DatabaseConnector, 
DataExtractor and DatabaseCleaning) to retrive data from a variety of sources, clean 
it and upload a dataframe to the sales_data database in the relational database management 
system PostgreSQL.'''

### 1. Creating a connection to the AWS database

## Create an instance of DatabaseConnector class
database_connector = DatabaseConnector()

## Use read_db_creds mehtod to return yaml credentials in useable format
yaml_creds = database_connector.read_db_creds('db_creds.yaml')
#print(yaml_creds) 

## Use these credentials to create an SQLAlchemy database engire to connect to the RDS
engine = database_connector.init_db_engine('db_creds.yaml')
#print(engine)

## List the table names that are in the AWS RDS database
get_table_names = database_connector.list_db_tables('db_creds.yaml')
#print(get_table_names) # ['legacy_store_details', 'legacy_users', 'orders_table']

### 2. Retrive, clean and upload the user data

## Retrieve database from the cloud
# create instance of DataExtractor class 
extract_rds_data = DataExtractor()
# Get one table name 
legacy_users_table_name = get_table_names[1]
# use it to read in/retrieve the data from the RDS table, which returns a dataframe
users_df = extract_rds_data.read_rds_table(database_connector, legacy_users_table_name, engine)
#print(users_df.head())




