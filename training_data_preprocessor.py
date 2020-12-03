import pandas as pd


info_data = pd.read_csv('csv_files/product_info.csv')

info_data = info_data[~info_data['product_rating'].str.contains(
    r'\?\?+ ', na=False)]

info_data['product_price'] = info_data['product_price'].replace(
    r'\?\?+|[,]|-.*', '', regex=True)

info_data = info_data[info_data['product_name'].notna(
) & info_data['product_price'].notna()].reset_index(drop=True)

info_data.to_csv('csv_files/database.csv', index_label='id')

training_data = info_data[['product_name', 'product_brand',
                           'product_type', 'product_rating', 'product_price']]

num_cols = ['product_rating', 'product_price']
string_cols = ['product_name', 'product_brand', 'product_type']

training_data[num_cols] = training_data[num_cols].astype('float')

training_data[string_cols] = training_data[string_cols].astype('string')

training_data.to_csv('csv_files/training.csv', index=False)
