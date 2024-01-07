import yaml
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect

class DatabaseConnector:
    '''
    A class which can be used to connect with and upload data to the database. 

    Methods:
    --------
    ''' 

    # This method returns a yaml file as a dictionary
    def read_db_creds(self, file):
        
        # Open YAML file in read mode
        with open(file, 'r') as stream: 
            # Use PyYAML's safe_load to parse the YAML content into a Python dictionary
            data_loaded = yaml.safe_load(stream)
    
        return data_loaded
    
    # This method uses the yaml dictionary to create a sqlachemy database engine
    def init_db_engine(self, file):
        
        # Read database credentials from the specified YAML file
        dict_yaml_func = self.read_db_creds(file)

        # Create a SQLAlchemy engine using the database credentials
        engine = create_engine(f"postgresql+psycopg2://{dict_yaml_func['USER']}:{dict_yaml_func['PASSWORD']}@{dict_yaml_func['HOST']}:{dict_yaml_func['PORT']}/{dict_yaml_func['DATABASE']}")
        # Connect to the database using the engine
        engine.connect()

        return engine
    
    # This method lists all the tables in the database to identify tables for data extraction
    def list_db_tables(self, file):

        # Create the database engine
        engine = self.init_db_engine(file) 
        # Inspect the structure of the database
        inspector = inspect(engine)
        # Get a list of table names in the 'public' schema
        table_names = inspector.get_table_names() 

        # Connect to the database and use an SQL query to retrieve table names
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            list_of_tables = []
            for table in result:
                list_of_tables.append(table)
        unpacked_tuples_list = [table[0] for table in list_of_tables]
        
        return unpacked_tuples_list
    
    ## This method takes in a Pandas DataFrame, table name and my crednetials for sales_data db and uploads it to PostgreSQL
    def upload_to_db(self, input_df, table_name, file):
            
        eng_con = self.init_db_engine(file)
        # creates table
        input_df.to_sql(table_name, eng_con, if_exists='replace', index=False)  

