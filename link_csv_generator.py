import pandas as pd
from product_link_scraper import link_scraper

sections = ['computing', 'electronics', 'phones-tablets',
            'category-fashion-by-jumia', 'groceries',
            'home-office', 'health-beauty', 'automobile',
            'sporting-goods', 'video-games', 'baby-products']

links_list = []

for section in sections:
    links_list.extend(link_scraper(50, section))

links_dict = {'links': links_list}

df = pd.DataFrame(links_dict)

df.drop_duplicates(inplace=True)

# saving the dataframe
df.to_csv('csv_files/links.csv', index=False)
