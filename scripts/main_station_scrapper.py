from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

def create_dataframe_schema():
    """
    Create dataframe schema
    """
    return pd.DataFrame(columns=['Station_id', 'Name'])

def create_soup(url):
    """
    Create soup object from url
    """
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except Exception as e:
        print("[ERROR] Error occurred in requesting html from SBB, requested url: {} is unavailable.".format(url))
        print("[ERROR] Error message: {}".format(e))

def get_station_id(soup,schema):
    """
    Get station id from soup object
    """
    parent_list= soup.find('ul', {'class': 'mod_station_search_results_list'})
    next=parent_list.find_next('li', {'class': 'mod_station_search_results_list_item'})
    while next is not None:
        if next.find('a', {'class': 'mod_station_search_results_list_item_link'}) is not None:
            station_id =next.find('a', {'class': 'mod_station_search_results_list_item_link'}).get('href').split('/')[-1].split('.')[1]
            station_name=next.find('a', {'class': 'mod_station_search_results_list_item_link'}).get_text()
            schema.loc[len(schema)] = [station_id, station_name]
        next=next.find_next('li', {'class': 'mod_station_search_results_list_item'})
    return schema

def scrape_main_station_page(base_url,schema):
    """
    Scrape main station page
    """
    soup = create_soup(base_url)
    schema = get_station_id(soup,schema)
    return schema

if __name__ == "__main__":
    #We extract the stations ids and names from the SBB Bedienpunktesuche page
    base_url='https://www.sbbcargo.com/de/kundencenter/tools/bedienpunktesuche.html'
    schema= create_dataframe_schema()
    df=scrape_main_station_page(base_url,schema)
    df.to_csv('../data/scrapped_data/main_stations_scrapper.csv')
