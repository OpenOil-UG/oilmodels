from django.db import models
from django_countries.fields import CountryField
from django.contrib.postgres.fields import HStoreField, ArrayField
from datetime import datetime
from ooapi import datextract

from django.conf import settings

import os, string,random
from six.moves.urllib import request
BASEDIR='/tmp/concession_search_pages'


if not os.path.exists(BASEDIR):
    os.makedirs(BASEDIR)

class ConcessionSearchResult(models.Model):
    concession = models.ForeignKey('Concession')
    source = models.CharField(
        choices = (('bing', 'Bing'),),
        max_length=20)
    date_scraped = models.DateField(default=datetime.now)
    date_original = models.DateField(null=True,blank=True) # date on the original page
    reviewed = models.BooleanField(default=False)
    blacklisted = models.BooleanField(default=False)
    url = models.URLField()
    title = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title

    def cached_page_fn(self):
        '''
        find the filename where we can store a cached version of the page
        '''
        dirname = os.path.join(BASEDIR, self.source)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        fn = '%s/%s.html' % (dirname, self.id)
        return fn

    def cached_page(self):
        fn = self.cached_page_fn()
        if os.path.exists(fn):
            return open(fn).read()
        # populate the cache
        text = request.urlopen(self.url).read()
        open(fn, 'wb').write(text)
        return text

    def guess_date(self, overwrite=False):
        if (overwrite is False) and self.date_original:
            return
        self.date = datextract.date_from_html(self.cached_page())

def new_key():
    return 'oo_' + ''.join(random.choice(string.lowercase+string.digits) for x in range(17))
        
class APIKey(models.Model):
    key = models.CharField(unique=True, max_length=25, default=new_key)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Concession(models.Model):
    name = models.CharField(max_length=200) # official govt. identifier
    country = CountryField(blank=True,null=True)
    type = models.CharField(max_length=30,
                            null=True,
                            blank=True,
                            choices = (
        ('onshore', 'Onshore'),
        ('offshore', 'Offshore'),))
    status = models.CharField(max_length=30, null=True,blank=True,choices=(
        ('licensed', 'Licensed'),
        ('unlicensed', 'Not Licensed'),
        ))
    source_document = models.CharField(max_length=300,
                                       null=True, blank=True) #url
    source_date = models.DateField(null=True,blank=True)
    retrieved_date = models.DateField(null=True,blank=True)
    further_info = models.TextField(null=True, blank=True) #for raw txt only; do not use
    details = HStoreField(null=True,blank=True)
    licensees = models.TextField(null=True,blank=True) # makes Baby Jesus cry

    def infodict(self):
        # basic info ready for json
        data = {}
        for field in (
                'name', 'type', 'status',
                'source_document', 'source_date',
                'retrieved_date', 'details'
        ):
            data[field] = getattr(self, field) or ""
        data['identifier'] = self.identifier()
        data['url_api'] = 'http://api.openoil.net/concession/%s' % data['identifier']
        data['url_wiki'] = self.url_wiki()
        data['country'] = self.country.code
        data['licensees'] = [x.strip() for x in self.licensees.split(',')]
        return data


    def identifier(self):
        return '%s/%s' % (self.country.code, self.name)

    def url_wiki(self):
        country_name = self.country.name #XXX check for naming mismatches
        return 'http://repository.openoil.net/wiki/%s' % country_name
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.country)

    
