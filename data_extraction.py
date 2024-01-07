from database_utils import DatabaseConnector
import pandas as pd

class DataExtractor:
    '''
    This class can be used to extract data from different data sources including CSV files, an API and an S3 bucket.

    Methods:
    --------
    ''' 

    # This method 
    def read_rds_table(self, instance_of_DbCon_class, table_name, engine_instance):
        if table_name == "legacy_users":
            df_legacy_users = pd.read_sql_table(table_name="legacy_users", con=engine_instance) 
            return df_legacy_users
        elif table_name == "orders_table":
            orders_df = pd.read_sql_table(table_name="orders_table", con=engine_instance)
            return orders_df
        elif table_name == "legacy_store_details":
            legacy_stores_df = pd.read_sql_table(table_name="legacy_store_details", con=engine_instance)
            return legacy_stores_df


