from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

def create_dataframe_schema():
    """
    Create dataframe schema
    """
    return pd.DataFrame(columns=['Name_Store', 'Address',])

def create_soup(url):
    """
    Create soup object from url
    """
    try:
        html_report_part1 = open(url,'r')
        soup = BeautifulSoup( html_report_part1, "html.parser")
        return soup
    except Exception as e:
        print("[ERROR] Error occurred in requesting html from Migros, requested url: {} is unavailable.".format(url))
        print("[ERROR] Error message: {}".format(e))

def get_station_id(soup,schema):
    """
    Get station id from soup object
    """
    
    parent_list= soup.find('div', {'class': 'sc-jefHZX gWbqRS'})
    next=parent_list.find_next('li', {'class': 'sc-hJZKUC feWXVV'})
    while next is not None:
        if next.find('a', {'class': 'sc-bXdNzS JsFoM'}) is not None:
            station_id =next.find('span', {'class': 'sc-fvpsdx hZOmlY'}).get_text()
            station_name=next.find('p', {'class': 'sc-ihINtW cMWzIG'}).get_text()
            schema.loc[len(schema)] = [station_id, station_name]
        next=next.find_next('li', {'class': 'sc-hJZKUC feWXVV'})
    return schema

def scrape_main_station_page(base_url,schema):
    """
    Scrape stores page
    """
    soup = create_soup(base_url)
    schema = get_station_id(soup,schema)
    return schema

if __name__ == "__main__":
    #We extract the stores addresses and names from the Migros page
    base_url='./html_migros/index_migros.html'
    schema= create_dataframe_schema()
    df=scrape_main_station_page(base_url,schema)
    df.to_csv('../data/scrapped_data_migros/stores_scrapper.csv')
