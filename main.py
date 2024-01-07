from data_cleaning import DatabaseCleaning
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
#extract_rds_data = DataExtractor()
# Get the users table name 
#legacy_users_table_name = get_table_names[1]
# use it to read in/retrieve the data from the RDS table, which returns a dataframe
#users_df = extract_rds_data.read_rds_table(database_connector, legacy_users_table_name, engine)
#print(users_df.head())

## clean user data
## create a csv file of the dataframe to visualise precleaned data
#users_df.to_csv('precleaned_user_data.csv')
## open csv file using VSCode excel view extension and explore the data
## create a ipynb file to experiemnt with the data cleaning before creating the method in the class
## run 'import pandas as pd' ''df = pd.read_csv('precleaned_user_data.csv')' 'df' and then create the method
## create an instance of DatabaseCleaning class
#clean_user = DatabaseCleaning()
# use clean_user_data() method to clean the data, and check the output by viewing the cleaned data
#clean_user_df = clean_user.clean_user_data(users_df)
#print(clean_user_df.head())
## check the data again by creating another csv file and examining it
#clean_user_df.to_csv('cleaned_user_data.csv')

### FUNCTION EXTRACTION FOR INCREASED READABILITY
### 2. Retrive, clean and upload the user data from an AWS database in the cloud.

def user_data():

    # create instance of DataExtractor class 
    extract_rds_data = DataExtractor()
    # Get the users table name
    legacy_users_table_name = get_table_names[1]
    # Use it to read in/retrieve the data from the RDS table, which returns a dataframe
    users_df = extract_rds_data.read_rds_table(database_connector, legacy_users_table_name, engine)

    # Create an instance of DatabaseCleaning class
    clean_user = DatabaseCleaning()
    # use clean_user_data() method to clean the data
    clean_user_df = clean_user.clean_user_data(users_df)

    # Upload to a new table called dim_users in SQAlchemy sales_data database.
    database_connector.upload_to_db(clean_user_df, "dim_users", 'my_creds.yaml')
    return clean_user_df

cleaned_users = user_data()
print(cleaned_users.head())



