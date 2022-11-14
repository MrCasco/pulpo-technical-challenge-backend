import datetime

from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv('API_KEY')
res = {2010+n: {} for n in range(20)}

def _get_sudan_donatives():
    iati_data = get_data_from_iati()['response']
    return iati_data
    for doc in iati_data['docs']:
        dates = doc['transaction_transaction_date_iso_date']
        orgs = doc['participating_org_narrative']
        transactions = doc['transaction_value']
        for org, transaction, date in zip(orgs, transactions, dates):
            year, _, _ = date.split('-')
            year = int(year)
            if year > 2017:
                res[year][org] = transaction
    return res

def get_data_from_iati():
    headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    url = 'https://api.iatistandard.org/datastore/transaction/select?q=recipient_country_code:SD&q.op=OR&sow=false&wt=json&group=false&facet=false&facet.sort=count&facet.missing=false&facet.method=fc&facet.range.other=none HTTP/1.1'
    r = requests.get(url=url, headers=headers)
    return r.json()
