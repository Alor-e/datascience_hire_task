import pandas as pd
from product_info_scraper import page_scraper


def csv_generator(start, end):
    """
    Generates a csv file containing the scraped data per product.
    """
    for n in range(start, end+1):

        link_df = pd.read_csv(f'input_split_csv/links_index-{n}.csv')

        link_df['product_name'], link_df['product_brand'],\
            link_df['product_type'], link_df['product_rating'],\
            link_df['product_price'], link_df['image_link'] = zip(
            *link_df['links'].apply(page_scraper))

        link_df.to_csv(f'output_split_csv/P{n}.csv', index=False)
        print(link_df)
        print(str(n) + ' csv files-----------------------------')


csv_generator(1, 218)
