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

