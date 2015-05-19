from ooapi import models
import csv
import pycountry
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
import requests
import traceback
import csv
import sys

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


def get_key_dict():
    fn = os.path.dirname(__file__) + '/concessionvalues_key.csv'
    reader = csv.DictReader(open(fn))
    keydata = {}
    for line in reader:
        k = line['original term']
        res = {
            'type': line['type'],
            'status': line['status']}
        keydata[k] = res
    return keydata

def fix_statuses():
    # each processor returns a dict of with keys 'status'
    # and 'type'. We combine these
    kd = get_key_dict()
    for row in models.Concession.objects.all():
        if 'Type' not in row.details:
            continue
        results = []
        
        for input_field in ('Type', 'Status'):
            results.append(
                kd.get( row.details.get(input_field, '').lower(), {})
            )
            
        for output_field in ('type', 'status'):
            for result in results:
                if result.get(output_field, None):
                    print('got %s %s %s' % (row, output_field, result[output_field]))
                    setattr(row, output_field, result[output_field])
                    break
        row.save()

        
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


def fix_furtherinfo():
    # break down the
    # from: u'Operador:Petra Energia, Concession\xe1rios:*Petra Energia - 100%, Contrato:BT-SF-3, Vencimento1\xba:12.03.2010, Observacao:EM AN\xc1LIS
    # to: {u'Concession\xe1rios': u'*Petra Energia - 100%',
    #   u'Contrato': u'BT-SF-3',
    #   u'Observacao': u'EM AN\xc1LISE',
    #   u'Operador': u'Petra Energia',
    #   u'Vencimento1\xba': u'12.03.2010'}

    for row in models.Concession.objects.all():
        d = {}
        parts = reversed([x.strip() for x in row.further_info.split(',')])
        remainder = u''
        for part in parts:
            if ':' in part:
                k,v = part.split(':', 1)
                d[k] = (v + remainder).strip()
                remainder = u''
            else: #this is something we got from not escaping commas
                remainder = remainder +', ' + part
        row.details = d
        row.save()




def keycounts():
    # stats on the keys found in the details field
    d = Counter()
    countries = defaultdict(set)
    for row in models.Concession.objects.all():
        for k in row.details.keys():
            d[k] += 1
            countries[k].add(row.country.code)
    for(label,count) in d.most_common(100):
        print(label,count,', '.join(countries[label]))
    return d

def valuecounts(field):
    #we want a count of every value in the field, plus the
    countries = defaultdict(set)
    counts = Counter()
    for row in models.Concession.objects.all():
        value = row.details.get(field,None)
        if not value:
            continue
        value = value.strip().lower()
        counts[value] +=1
        countries[value].add(row.country.code)
    w = csv.writer(open('/tmp/concessionvalues_%s.csv' % field.lower(),'w'))
    for (label, count) in counts.most_common():
        w.writerow([label, count, ', '.join(countries[label])])
