'''
Monthly production from Tunisia
'''
import datetime
import requests
import lxml.html
import re
from modeling import models
from django_date_extensions.fields import ApproximateDate

def decompose_table(table):
    results = []
    for row in table.findall('tr'):
        rowdata = []
        for cell in row.findall('td'):
            rowdata.append(cell.text_content().strip())
        results.append(rowdata)
    return results

def partners(rows):
    partners = []
    state = 'IGNORE'
    for row in rows:
        if state == 'IGNORE':
            if 'Partenaire' not in row[0]:
                continue
            state = 'TAKE'
        elif len(row) < 3:
            state = 'IGNORE'
        partners.append(row[-2:])
    return partners

def get_by_regex(d, regex):
    for k,v in d.items():
        if re.match(regex, k):
            return v

def one_concession(num):
    url = 'http://www.etap.com.tn/index.php?id=1160&fiche=%s' % num
    pagetext = requests.get(url).text
    # XXX archive the page text somewhere
    data = {
        'source_url': url,
        'scrape_date': datetime.datetime.now()}
    lx = lxml.html.fromstring(pagetext)
    data['field_name'] = lx.cssselect('h4>strong')[0].text
    table = lx.cssselect('table.tab_concess')[0]
    table_rows = decompose_table(table)
    table_dict = dict([(x[0], x[1:]) for x in table_rows])
    for ourlabel, theirlabel in (
            ('license_area','Permis'),
            ('number_of_wells','Puits de production'),
            ('production_type','Situation'),
            ('operator','Opérateur'),
            ('production_start_date','La mise en production'),
            ('discovery_date','Date de découverte'),
    ):
        if theirlabel in table_dict:
            data[ourlabel] = table_dict[theirlabel][-1]
        else:
            data[ourlabel] = ''

    data['production_per_day'] = get_by_regex(table_dict, 'Production journaliére Moyenne.*')[-1]
    prod_nums = re.search('([\d ]+)', data['production_per_day'])
    if prod_nums:
        data['production_per_day_normalized'] = int(''.join(x for x in prod_nums.group() if x.isdigit()))
    data['production_data_date'] = re.search('Production journaliére Moyenne \((\d+)\)', table.text_content()).group(1)
    
    data['partners'] = partners(table_rows)
    return data


def importall():
    for num in range(1,120):
        data = one_concession(num)
        if not data['field_name']:
            continue
        field, created = models.Project.objects.get_or_create(
            project_name = data['field_name'].title(),
            type='field',
            country='TN')
        for partner in data['partners']:
            partner_name = partner[0].title()
            try:
                partner_share = int(''.join(x for x in partner[1] if x.isdigit()))
            except Exception:
                partner_share = None
            company, created = models.Company.objects.get_or_create(
                company_name = partner_name)

            if data['production_per_day'] == '':
                print('no production figure available')
                continue
            prod, created = models.Production.objects.get_or_create(
                project=field,
                company=company,
                date=ApproximateDate(
                    year=int(data['production_data_date'])),
                commodity='oil', #XXX is it always?
                actual_predicted='actual',
                level=data['production_per_day_normalized'],
                per='day',)
            prod.save()
        print('imported %s' % num)
                
                
                
        
        
