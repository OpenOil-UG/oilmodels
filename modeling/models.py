from django_pg import models
from django.contrib.postgres.fields import DateRangeField
from django_countries.fields import CountryField

# Create your models here.

class DataSource(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    url_homepage = models.URLField(blank=True,null=True)
    url_example = models.URLField(blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    #daterange = DateRangeField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class InformationType(models.Model):
    DataSource = models.ForeignKey('DataSource', related_name='information_types')
    name = models.CharField(max_length=200, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    filing_type = models.CharField(max_length=200, blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    patterns = models.TextField(blank=True,null=True)
    examples = models.TextField(blank=True,null=True)
    negative_examples = models.TextField(blank=True,null=True)
    regulations = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

    
class Reserve(models.Model):
    # convert all reserves to million barrels BEFORE importing
    p1 = models.FloatField(blank=True,null=True)
    p2 = models.FloatField(blank=True,null=True)
    p3 = models.FloatField(blank=True,null=True)

    year = models.IntegerField(blank=True,null=True)

    field_name = models.CharField(max_length=200, blank=True,null=True)
    project_name = models.CharField(max_length=200, blank=True,null=True)
    company_name = models.CharField(max_length=200, blank=True,null=True)
    company_name = models.CharField(max_length=200, blank=True,null=True)

    reporting_level = models.CharField(max_length=100,
                                       choices = (
                                           ('field', 'Field'),
                                           ('project', 'Project'),
                                           ('company-country', 'Company (in one country)'),
                                           ('company', 'Company (global)'),
                                           ('country', 'Country (all companies'))
                                       )

    country = CountryField(blank=True,null=True)

    #source = models.ForeignKey('Source')

    

    
