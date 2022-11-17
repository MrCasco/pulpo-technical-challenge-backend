import datetime

from dotenv import load_dotenv
import os
import requests

from collections import defaultdict
from currency_converter import CurrencyConverter


load_dotenv()

API_KEY = os.getenv('API_KEY')
MAXIMUM_WINDOW = 10

def _get_donatives(start_date, country_code):
    # This is the result dictionary labeled by each year from start_date to start_date-5
    result = {start_date-n-1: defaultdict(lambda: 0) for n in range(MAXIMUM_WINDOW)}
    # Raw data obtained from the IATI API
    iati_data = _get_data_from_iati(start_date, country_code)['response']

    for doc in iati_data['docs']:
        dates = doc['transaction_value_value_date']
        orgs = _get_donative_orgs(doc)
        transactions = _convert_to_dollars(doc['transaction_value'], doc['default_currency'])

        # Sometimes the transaction array has less data than orgs, hence, solution is dividing the total sum by all the orgs
        if len(transactions) < len(orgs):
            trans_sum = sum(transactions)
            transactions = [trans_sum/len(orgs) for _ in range(len(orgs))]

        for org, transaction, date in zip(orgs, transactions, dates):
            year, _, _ = date.split('-')
            year = int(year)
            if start_date-MAXIMUM_WINDOW < year < start_date:
                result[year][org] += transaction
    _order_by_donation_value(res)
    return result


def _get_data_from_iati(start_date, country_code):
    headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    url = 'https://api.iatistandard.org/datastore/transaction/select?q=(recipient_country_code:'+country_code+')AND(activity_date_iso_date:['+str(start_date-MAXIMUM_WINDOW)+'-01-01T00:00:00Z TO '+str(start_date-1)+'-01-01T00:00:00Z])&q.op=OR&sow=false&rows=100&wt=json&group=false&facet=false&facet.sort=count&facet.missing=false&facet.method=fc&facet.range.other=none HTTP/1.1'
    r = requests.get(url=url, headers=headers)
    return r.json()


def _get_donative_orgs(doc):
    res = []
    # Sometimes 'transaction_provider_org_narrative' does not exist, then switch to 'participating_org_narrative'
    org_field = 'transaction_provider_org_narrative' if 'transaction_provider_org_narrative' in doc else 'participating_org_narrative'

    for org, role in zip(doc[org_field], doc['participating_org_role']):
        # We check for role == 1 because documentation says its the corresponding role for "Funding"
        if role == '1':
            res.append(org)
    return res


def _order_by_donation_value(res):
    for year, donators in res.items():
        res[year] = {k: res[year][k] for k in sorted(res[year], key=res[year].get, reverse=True)}


def _convert_to_dollars(amount, initial_currency):
    return CurrencyConverter().convert(amount, initial_currency, 'USD')
