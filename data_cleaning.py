import pandas as pd
from dateutil.parser import parse

class DatabaseCleaning:
    '''
    This class can be used to clean data from a variety of Amazon Web Services (AWS) data sources.

    Methods:
    --------
    '''

    def clean_user_data(self, user_df):
        '''
        Cleans and preprocesses user data in the provided DataFrame.

        Parameters:
        -----------
        user_df : pandas.DataFrame
        The input DataFrame containing user data.

        Returns:
        --------
        pandas.DataFrame
            A cleaned DataFrame with the following operations performed:
            1. Set "index" column as the DataFrame index.
            2. Filter rows based on specified countries.
            3. Convert selected columns to the string datatype.
            4. Convert date columns to datetime format.'''
        
        # Set index as index
        user_df = user_df.set_index('index')

        # Create mask and apply it to get rid of invalid rows and NULL/NaN
        selected_countries = ["Germany", "United Kingdom", "United States"]
        country_mask = user_df.loc[:,"country"].isin(selected_countries) # ,: means search all rows in just country
        user_df_mask = user_df[country_mask]

        ## convert most columns to string datatype
        # create dictionary to map column name to dataype
        col_data_types = {'first_name': 'string', 'last_name': 'string', 'company':'string', 'email_address':'string', 'address':'string', 'country':'string', 'country_code':'string','phone_number':'string','user_uuid':'string'}
        # use a for loop to iterate through the columns and change the dtype
        for column, data_type in col_data_types.items():
            user_df_mask[column] = user_df_mask[column].astype(data_type)

        ## convert date columns to datetime
        user_df_mask['date_of_birth'] = user_df_mask['date_of_birth'].apply(parse)
        user_df_mask['date_of_birth'] = user_df_mask['date_of_birth'].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce')
        user_df_mask['join_date'] = user_df_mask['join_date'].apply(parse)
        user_df_mask['join_date'] = user_df_mask['join_date'].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce') # .apply() applies a function, with arguments inside brackets
        # this prevents the rows being turned into nulls and then deleted.
    
        return user_df_mask

    def clean_card_data(self, card_df):
       
        # mask to filter card_provider to delete invalid data and null rows
        card_provider_list = ["American Express","Diners Club / Carte Blanche", "Discover", "JCB 15 digit", "JCB 16 digit", "Maestro", "Mastercard", "VISA 13 digit", "VISA 16 digit", "VISA 19 digit"]
        card_mask = card_df.loc[:,"card_provider"].isin(card_provider_list)
        df_mask = card_df[card_mask]

        # drop the '?' characters in invalid card_numbers
        # to search specifically for character, convert to string
        df_mask['card_number'] = df_mask['card_number'].astype('string')
        replacements = [("?", "")]
        for char, replacement in replacements:
            df_mask["card_number"] = df_mask["card_number"].str.replace(char, replacement)
        # convert into int64
        df_mask['card_number'] = df_mask['card_number'].astype('int64')

        # turn other cols into strings 
        col_data_types = {'expiry_date':'string', 'card_provider':'string'}
        for column, data_type in col_data_types.items():
            df_mask[column] = df_mask[column].astype(data_type)
        
        # cast columns to datetime
        df_mask['date_payment_confirmed'] = df_mask['date_payment_confirmed'].apply(parse)
        df_mask['date_payment_confirmed'] = df_mask['date_payment_confirmed'].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce') 

        return df_mask

    def clean_store_data(self, store_df):
        
        # drop lat column as it's empty and latitude col is also there
        store_info_df_no_lat = store_df.drop('lat', axis=1)

        # create store_type mask for cleaning strange data and nulls 
        store_type_list = ["Local", "Mall Kiosk", "Super Store", "Outlet", "Web Portal"]
        store_type_mask = store_info_df_no_lat.loc[:,"store_type"].isin(store_type_list)
        store_info_mask = store_info_df_no_lat[store_type_mask]
    
        # ValueError: could not convert string to float: 'N/A'
        # drop N/A from longitude or latitude at index 0
        store_info_mask_nona = store_info_mask.drop([0], axis=0) # had to re-enter this row in SQL

        # convert columns to string and flaot64
        col_data_types = {"latitude":"float64", "longitude":"float64", "address":"string", "locality":"string", "store_code":"string", "store_type":"string", "country_code":"string", "continent":"string"}
        for column, data_type in col_data_types.items():
            store_info_mask_nona[column] = store_info_mask_nona[column].astype(data_type)

        # staff_number has values with "accidental" letters mixed in so can't convert to int64
        store_info_mask_nona['staff_numbers'] = store_info_mask_nona['staff_numbers'].replace(["J78", "30e", "80R", "A97", "3n9"], ["78", "30", "80", "97", "39"])
        # convert to int64
        store_info_mask_nona['staff_numbers'] = store_info_mask_nona['staff_numbers'].astype("int64")
        #print(store_info_mask_nona.info())

        # change opening_date to datetime64
        store_info_mask_nona['opening_date'] = store_info_mask_nona['opening_date'].apply(parse)
        store_info_mask_nona['opening_date'] = store_info_mask_nona['opening_date'].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce') 

        return store_info_mask_nona


    def convert_product_weights(self, df):
        # create new columns, using regex to seperate weight and unit
        df['numeric_value'] = pd.to_numeric(df['weight'].str.extract('(\d+.\d+|\d+)')[0], errors='coerce') # casts as a float 
        df['unit'] = df['weight'].str.extract('([a-zA-Z]+)')
        
        # define dictionary for conversion
        conversion_factors = {'ml': 0.001, 'g': 0.001, 'kg': 1, 'k': 1}
        
        df.loc[df['unit'] == 'ml', 'numeric_value'] *= conversion_factors['ml']
        # for every row where ['unit'] equals ml, it multiplies the corresponding 'numeric_value' row by the value of the 'ml' key in the conversion_factors dictionary
        df.loc[df['unit'] == 'g', 'numeric_value'] *= conversion_factors['g']
        df.loc[df['unit'].isin(['kg', 'k']), 'numeric_value'] *= conversion_factors['kg']

        df['weight_kg'] = df['numeric_value']

        # drop unnecessary columns
        df.drop(['weight', 'numeric_value', 'unit'], axis=1, inplace=True)
        
        return df
    
    def clean_products_data(self, df):
    
        # create mask to filter invalid data using removed column:
        # first correct spelling mistake of 'avaliable'
        df["removed"] = df["removed"].astype("string")
        df["removed"] = df["removed"].str.replace('Still_avaliable', 'Still_available', regex=True)
        # filter
        availability_list = ["Still_available", "Removed"] 
        availability_mask = df.loc[:,"removed"].isin(availability_list)
        product_mask_df = df[availability_mask]

        # remove £ from price column and convert to float64
        # cast as string
        product_mask_df["product_price"] = product_mask_df["product_price"].astype("string")
        # create new col from it while removing the £ sign
        product_mask_df["product_price_sterling"] = product_mask_df["product_price"].str.replace("£", "", regex=True)
        # convert to float
        product_mask_df["product_price_sterling"] = product_mask_df["product_price_sterling"].astype(float)
        # delete 'product_price' column
        product_mask_df = product_mask_df.drop(["product_price"], axis=1)

        # cast columns to correct datatype apart from datetime
        col_data_types = {'product_name':'string', 'category':'string', 'EAN':'string', 'uuid':'string', 'product_code':'string'}
        for column, data_type in col_data_types.items():
            product_mask_df[column] = product_mask_df[column].astype(data_type)

        # make all product_code upper()
        product_mask_df["product_code"] = product_mask_df["product_code"].str.upper()
            
        # impute data for the weights which are 0kg, using mean
        #product_mask_df["weight_kg"].describe()
        product_mask_df["weight_kg"] = product_mask_df["weight_kg"].fillna(product_mask_df["weight_kg"].mean())  # mean = 3.15

        # cast datetime
        product_mask_df['date_added'] = product_mask_df['date_added'].apply(parse)
        product_mask_df['date_added'] = product_mask_df['date_added'].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce') 
        
        return product_mask_df



