from data_cleaning import DatabaseCleaning
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
import matplotlib.pyplot as plt
import numpy as np
import yaml

''' This is the script where I will use the three different classes (DatabaseConnector,
DataExtractor and DatabaseCleaning) to retrive data from a variety of sources, clean 
the data and upload to the sales_data database in the relational database management 
system PostgreSQL.'''

### 1. Creating a connection to the AWS database

# Create an instance of DatabaseConnector class
database_connector = DatabaseConnector()
# Use read_db_creds mehtod to return yaml credentials in useable format
yaml_creds = database_connector.read_db_creds('db_creds.yaml')
# Use these credentials to create an SQLAlchemy database engire to connect to the RDS
engine = database_connector.init_db_engine('db_creds.yaml')
# List the table names that are in the AWS RDS database
get_table_names = database_connector.list_db_tables('db_creds.yaml')
#print(get_table_names) # ['legacy_store_details', 'legacy_users', 'orders_table']

### 2. Retrive, clean and upload the user data from an AWS database in the cloud.

def user_data():
    '''
    This function retrieves, cleans, and uploads user data from an AWS RDS database to a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing user data, which has also been uploaded to the "dim_users" table.
    '''
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


### 3. Retrive, clean and upload the card data from a PDF document in an AWS S3 bucket

def card_data():
    '''
    This function retrieves, cleans, and uploads card data from a PDF document in an AWS S3 bucket into a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing card data, which has also been uploaded to the "dim_card_details" table.
    '''
    # Create instance of DBConnector class
    extract_pdf_data = DataExtractor()
    # takes in uncleaned df as arg, sets it to cleaned_df variable
    card_details_df = extract_pdf_data.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    
    # Create Cleaning instanct
    card_cleaning = DatabaseCleaning()
    # Use clean_card_data method to clean df
    clean_card_df = card_cleaning.clean_card_data(card_details_df)
    
    # upload to a new table called dim_card_details in SQAlchemy sales_data database
    database_connector.upload_to_db(clean_card_df, "dim_card_details", 'my_creds.yaml')
    
    return clean_card_df


### 4. Extract, clean and upload store details from using an API

'''The store data can be retrieved through the use of an API.
The API has two GET methods. One will return the number of stores in the business and the other to retrieve a store given a store number.

The two endpoints for the API are as follows:
Retrieve a store: https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}
Return the number of stores: https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'''

# Use read_db_creds method to read yaml file with api key
api_header_details = database_connector.read_db_creds('api_key.yaml')
num_of_stores_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
api_retrieval = DataExtractor()
# Use the list_number_of_stores method to get the number of total stores
total_stores = api_retrieval.list_number_of_stores(num_of_stores_endpoint, api_header_details)
#print(total_stores) # 451

def stores_data():
    '''
    This function retrieves, cleans, and uploads stores data using an API into a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing store data, which has also been uploaded to the "dim_store_details" table.
    '''
    retrieve_store_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/" # number of stores will be added onto the end of this
    # Use retrieve_stores_data method to return the df
    store_info_df = api_retrieval.retrieve_stores_data(retrieve_store_endpoint, total_stores, api_header_details)

    # clean stores_df
    store_cleaning = DatabaseCleaning()
    clean_store_df = store_cleaning.clean_store_data(store_info_df)

    # Upload to a new table called dim_store_details in SQAlchemy sales_data database
    database_connector.upload_to_db(clean_store_df, "dim_store_details", 'my_creds.yaml')

    return clean_store_df


### 5. Extract, edit, clean and upload data from product details from csv file in s3 bucket

def product_data():
    '''
    This function retrieves, cleans, and uploads product data from a csv file in an s3 bucket into a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing product data, which has also been uploaded to the "dim_products" table.
    '''
    # S3 URI:
    s3_products_address = database_connector.read_db_creds('s3_url.yaml')

    # use the extract_from_s3 method to input the s3 address and return a dataframe
    get_product_details = DataExtractor()
    precleaned_product_df = get_product_details.extract_from_s3(s3_products_address)
    
    # Use convert_product_weights method to convert weights column to same unit (kg)
    clean_product_data = DatabaseCleaning()
    product_weight_kg_df = clean_product_data.convert_product_weights(precleaned_product_df)

    # Clean the rest of the dataframe
    cleaned_product_df = clean_product_data.clean_products_data(product_weight_kg_df)

    # upload to sales_data database using upload_to_db method in a table named dim_products
    database_connector.upload_to_db(cleaned_product_df, "dim_products", 'my_creds.yaml')

    return cleaned_product_df


### 6. Retrieve orders table from AWS RDS

def orders_data():
    '''
    This function retrieves, cleans, and uploads orders data from an AWS RDS into a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing orders data, which has also been uploaded to the "orders_table" table.
    '''
    # get table name associated with orders 
    orders_table_name = get_table_names[2]

    # create instance of DataExtractor class 
    extract_rds_data = DataExtractor()
    rds_orders_df = extract_rds_data.read_rds_table(database_connector, orders_table_name, engine)

    # use it to clean the df and return clean df
    clean_orders_df = DatabaseCleaning()
    orders_df = clean_orders_df.clean_orders_data(rds_orders_df)

    # Upload to sales_data database using upload_to_db method in a table named orders_table
    database_connector.upload_to_db(orders_df, "orders_table", 'my_creds.yaml')

    return orders_df


### 7. Retrieve, clean and upload date events data from JSON file in s3 bucket.

def date_data():
    '''
    This function retrieves, cleans, and uploads orders data from a JSON file in s3 bucket into a new table in the sales_data database.

    Returns:
        pandas.DataFrame: A cleaned DataFrame containing date data, which has also been uploaded to the "dim_date_times" table.
    '''
    # create a DataExtractor instance
    extract_json_data = DataExtractor()

    # Use read_db_creds method to get link to json object
    json_s3_address = database_connector.read_db_creds('json_s3_url.yaml')

    # use extract_from_s3 method to get a dataframe
    date_time_details_df = extract_json_data.extract_from_s3(json_s3_address)

    # Clean the data using clean_date_data 
    date_cleaning = DatabaseCleaning()
    clean_date_df = date_cleaning.clean_date_data(date_time_details_df)

    # Upload to sales_data database using upload_to_db method in a table named dim_date_times
    database_connector.upload_to_db(clean_date_df, "dim_date_times", 'my_creds.yaml')

    return clean_date_df

if __name__ == "__main__":
    date_data()
    orders_data()
    product_data()
    stores_data()
    card_data()
    user_data()

### 8. Create the Database Schema

# This will be run using the db_schema.sql file and includes casting column datatypes, adding descriptive columns, assigning primary and foreign keys.
    
### 9. Query the Database  

# Answering business questions about the sales 
# Here's a sneak peak at the result queary 5: What percentage of sales come through each type of store?

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    store_type = ['Local', 'Web Portal', 'Super Store', 'Mall Kiosk', 'Outlet']
    percentage_total = np.array([44.557729, 22.357841, 15.853934, 9.048969, 8.181527])
    ax.pie(percentage_total, labels=store_type, autopct='%1.2f%%')
    plt.show()