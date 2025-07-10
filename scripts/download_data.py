import requests
import pandas as pd
from math import ceil


def get_data(url: str):
    '''
    Fetches the data in JSON.
    '''
    response = requests.get(url)
    data = response.json()

    return data


def make_url(resource: str, parameters: dict) -> str:
    '''
    Creates URL for the GUS REST API - BDL API.
    '''
    endpoint = 'https://bdl.stat.gov.pl/api/v1/'
    pars = '&'.join(f'{k}={v}' for k, v in parameters.items())
    url =  endpoint + resource + '?' + pars

    return url


def get_num_pages(resource: str, parameters: dict) -> int:
    '''
    Get number of pages given by the GUS REST API - BDL API under  given URL.
    '''

    if 'page-size' in parameters.keys():
        page_size = parameters['page-size']
    else:
        page_size = 100

    url = make_url(resource, parameters)
    data = get_data(url)
    
    total_records = data['totalRecords']
    num_pages = ceil(total_records / page_size)

    return num_pages


def default_params() -> dict:

    params = {'lang':'en',
              'format':'json'}

    return params


def fetch_all(resource: str, parameters: dict) -> pd.DataFrame:
    '''
    Fetch all data for given resource and parameters via API.
    '''
    num_pages = get_num_pages(resource, parameters)

    paramaters = default_params() | parameters

    dfs = []

    for i in range(num_pages):
        parameters['page'] = i
        url = make_url(resource, parameters)

        data = get_data(url)['results']
        dfs.append(pd.json_normalize(data))

    df = pd.concat(dfs, ignore_index=True)

    return df
