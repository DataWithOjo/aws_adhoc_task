import pandas as pd
import awswrangler as wr
import boto3
import requests

s3_client = boto3.client('s3') 

session = boto3.Session(region_name="eu-north-1") 

baseurl = 'https://rickandmortyapi.com/api/'
endpoint = 'character'

def main_request(baseurl, endpoint, x):
    r = requests.get(baseurl + endpoint + f'?page={x}')
    return r.json()

def get_pages(response):
    return response['info']['pages']

def parse_json(response):
    charlist = []
    for item in response['results']:
        char = {
            'id': item['id'],
            'name': item['name'],
            'no_episode': len(item['episode']),
        }

        charlist.append(char)
    return charlist

mainlist = []
data = main_request(baseurl, endpoint, 1)
for x in range(1, get_pages(data)+1):
    response = main_request(baseurl, endpoint, x)
    mainlist.extend(parse_json(response))

characters_df = pd.DataFrame(mainlist)


# Write to s3 in Parquet Format and register in glue data catalog
wr.s3.to_parquet(
        df=characters_df,
        path="s3://cde-user-oluwakayode/characters_data/",
        boto3_session=session,
        mode="overwrite",
        database="cdeoluwakayodedb",
        table="cdeoluwakayodecatalogtable",
        dataset=True
    )