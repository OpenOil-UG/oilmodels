from django_pg import models
from django.contrib.postgres.fields import DateRangeField
from django_countries.fields import CountryField
from django.contrib.auth.models import User

from hulk.models import Document, Company, Project

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


class ReserveLevel(models.Model):
    # XXX Nameme!
    category = models.CharField(
        max_length=20,
        choices = ((x,x) for x in [
            'Unknown',
            '1P',
            '2P',
            '3P',
            '1C',
            '2C',
            '3C',
            ]),
        default='Unknown',
        )
    status = models.CharField(
        max_length=20,
        choices = (
            ('developed', 'Developed'),
            ('undeveloped', 'Undeveloped'),
            ('total', 'Total'),
            ('unspecified', 'Unspecified'),
            ),
        default = 'unspecified')

    level = models.FloatField()
    unit = models.CharField(
        max_length=20,
        choices = (
            ('mbbls', 'Million barels'),
            ('mmcf', 'Million cubic feet (mmcf/mmscf)'),
            ('mboe', 'Million barels oil equivalent'),
            ),
        default = 'mbbls')
    reserve = models.ForeignKey('Reserve', related_name='reserve_levels')

    
class Reserve(models.Model):
    # convert all reserves to million barrels BEFORE importing
    #p1 = models.FloatField(blank=True,null=True)
    #p2 = models.FloatField(blank=True,null=True)
    #p3 = models.FloatField(blank=True,null=True)

    project = models.ForeignKey(Project, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    year = models.IntegerField(blank=True,null=True,
                               help_text = "year statement applies to, if specified, otherwise publication year of the source document")
    country = CountryField(blank=True,null=True)
    commodity = models.CharField(max_length=100, choices = (
        ('gas', 'Gas'),
        ('oil', 'Oil, grade unspecified'),
        ('oil', 'Oil, heavy'),
        ('oil', 'Oil, light and medium'),
        ))
    interest = models.FloatField(default=100, verbose_name = "Interest of the company in this project (%)")
    source_document = models.ForeignKey(Document, blank=True, null=True)

    reporting_level = models.CharField(max_length=100,
                                       choices = (
                                           ('well', 'Well'),
                                           ('field', 'Field'),
                                           ('project', 'Project'),
                                           ('company-country', 'Company (in one country)'),
                                           ('company', 'Company (global)'),
                                           ('country', 'Country (all companies'))
                                       )



    def __str__(self):
        if self.project and self.project.project_name:
            return '%s: %s estimate' % (self.project.project_name, self.year)
        else:
            return 'unnamed'


    #source = models.ForeignKey('Source')

class Task(models.Model):
    source = models.ForeignKey(Document)
    status = models.CharField(max_length=12,
                              choices=[
                                  (x,x) for x in (
                                      'completed',
                                      'in progress',
                                      'available',
                                      'on hold')
                                  ])
    task_group = models.ForeignKey('TaskGroup')
    date_completed = models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User)
    data = models.JSONField(null=True,blank=True)

class TaskGroup(models.Model):
    description = models.CharField
    data = models.JSONField(null=True,blank=True)
    
