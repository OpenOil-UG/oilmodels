from django.db import models
from django_countries.fields import CountryField
# Create your models here.

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
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.country)

    
