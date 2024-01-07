from database_utils import DatabaseConnector
import pandas as pd
import tabula

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

    def retrieve_pdf_data(self, link):

        # use tabula to reads remote pdf into list of DataFrame using tabula
        self.link = link
        pdf_dataframe_list = tabula.read_pdf(self.link, pages='all') 
        pdf_dataframe = pd.concat(pdf_dataframe_list, ignore_index=True) # convert list into dataframe
        
        return pdf_dataframe



