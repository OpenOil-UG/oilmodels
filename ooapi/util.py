from ooapi import models
import csv
import pycountry
import re
from datetime import datetime
import requests
import traceback

APIKEY = 'VGm1FGzG9d6pZVqAxaQW10SVi9aaW6YJkPREI116aJA='


def query_bing(query):
    url = 'https://api.datamarket.azure.com/Bing/Search/Web'
    params = {
        'Query': "'%s'" % query,
        '$format': 'json',}
    auth = (APIKEY, APIKEY)
    result = requests.get(url, params=params, auth = auth)
    try:
        return result.json()['d']['results']
    except exception:
        print('bad result for query %s % query')
        traceback.print_exc()
        return []

def searchterm_for_conc(conc):
    return '"%s" "%s"' % (conc.name, conc.country.name)
    
def bing_concession(conc):
    searchterm = searchterm_for_conc(conc)
    for result in query_bing(searchterm):
        r = models.ConcessionSearchResult(
            concession = conc,
            source = 'bing',
            url = result['Url'],
            title = result['Title'],
            description= result['Description'],
        )
        r.save()

def get_country_code(fname):
    # '/path/to/Concessions_Zambia_17122014.csv' --> 'ZM'


    awkward_countries = {
        'Vietnam': 'VN',
        'South Korea': 'KR',
        'Falkland Isalnds': 'FK',
        'Democratic Republic of Cogo': 'CD',
        'Tanzania': 'TZ',
        'Ivory Coast': 'CI',
        }
    country_name = re.search('Concessions_(.*?)_', fname).group(1)
    if country_name in awkward_countries:
        return awkward_countries[country_name]
    country = pycountry.countries.get(name=country_name)
    return country.alpha2

def get_type(desc):
    match = re.search('Type: *([^:]+)', desc)
    if match is None:
        return None
    txt = match.group(1).lower()
    if 'offshore' in txt:
        return 'offshore'
    if 'onshore' in txt:
        return 'onshore'
    return None

def get_status(desc):
    match = re.search('Type: *([^:]+)', desc)
    if match is None:
        return None
    txt = match.group(1).lower()
    if any(x in txt for x in ('open', 'free', 'unlicensed')):
        return 'unlicensed'
    if any(x in txt for x in (
            'licensed', 'production', 'exploration',
            'prospecting')):
        return 'licensed'
    return None


def concession_from_csv(fname):
    reader = csv.DictReader(open(fname))
    isocountry = get_country_code(fname)
    for row in reader:
        source_date, retrieved_date = (None, None)
        try:
            source_date = datetime.strptime(row['ConcessionSourceDate'], '%d/%m/%Y')
        except ValueError:
            pass
        try:
            retrieved_date = datetime.strptime(row['Retrieved at'], '%d/%m/%Y')
        except ValueError:
            pass
        c = models.Concession(
            name = row['ConcessionName'].strip(),
            country = isocountry,
            source_document = row['ConcessionSource'],
            source_date = source_date,
            retrieved_date = retrieved_date,
            licensees = row['ConcessionContractor'],
            further_info = row['ConcessionDescription'],
            type = get_type(row['ConcessionDescription']),
            status = get_status(row['ConcessionDescription']),
            )
        c.save()

