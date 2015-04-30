from django.db import models
from django_countries.fields import CountryField
from datetime import datetime
# Create your models here.

class ConcessionSearchResult(models.Model):
    concession = models.ForeignKey('Concession')
    source = models.CharField(
        choices = (('bing', 'Bing'),),
        max_length=20)
    date_scraped = models.DateField(default=datetime.now)
    reviewed = models.BooleanField(default=False)
    blacklisted = models.BooleanField(default=False)
    url = models.URLField()
    title = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title

class Concession(models.Model):
    name = models.CharField(max_length=200)
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
    further_info = models.TextField(null=True, blank=True)
    licensees = models.TextField(null=True,blank=True) # makes Baby Jesus cry

    def infodict(self):
        # basic info ready for json
        data = {}
        for field in (
                'name', 'type', 'status',
                'source_document', 'source_date',
                'retrieved_date', 'licensees',
                'further_info'
        ):
            data[field] = getattr(self, field) or ""
        data['country'] = self.country.code
        return data

        
    def __str__(self):
        return "%s (%s)" % (self.name, self.country)

    
