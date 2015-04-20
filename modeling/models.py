from django_pg import models
from django.contrib.postgres.fields import DateRangeField
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django_date_extensions.fields import ApproximateDateField
from hulk.models import Document, Company, Project

COMMODITIES = (
        ('gas', 'Gas'),
        ('oil', 'Oil, grade unspecified'),
        ('oil', 'Oil, heavy'),
        ('oil', 'Oil, light and medium'),
        )

CONFIDENCE_MEASURES = [(x,x) for x in [
            'Unknown',
            '1P',
            '2P',
            '3P',
            '1C',
            '2C',
            '3C',
            ]]

FIELD_STATUSES = (
            ('developed', 'Developed'),
            ('undeveloped', 'Undeveloped'),
            ('total', 'Total'),
            ('unspecified', 'Unspecified'),
            )

UNITS = (
    ('mbbls', 'Million barels'),
    ('mmcf', 'Million cubic feet (mmcf/mmscf)'),
    ('mboe', 'Million barels oil equivalent'),
    ('tdf', 'Thousand Cubic Feet (mcf/mscf)'),
            )

REPORTING_LEVELS = (
    ('well', 'Well'),
    ('field', 'Field'),
    ('project', 'Project'),
    ('company-country', 'Company (in one country)'),
    ('company', 'Company (global)'),
    ('country', 'Country (all companies')
    )

TIME_PERIODS = (
    ('day', 'day'),
    ('month', 'month'),
    ('year', 'year'))

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

    project = models.ForeignKey(Project, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    interest = models.FloatField(default=100, verbose_name = "Interest of the company in this project (%)")
    date = ApproximateDateField(blank=True,null=True,
                               help_text = "year statement applies to, if specified, otherwise publication year of the source document")
    commodity = models.CharField(max_length=100, choices = COMMODITIES)
    confidence = models.CharField(
        max_length=20,
        choices = CONFIDENCE_MEASURES,
        default='Unknown',
        )
    status = models.CharField(
        max_length=20,
        choices = FIELD_STATUSES,
        default = 'unspecified')
    level = models.FloatField()
    unit = models.CharField(
        max_length=20,
        choices = UNITS,
        default = 'mbbls')
        
    source_document = models.ForeignKey(Document, blank=True, null=True)


    def __str__(self):
        if self.project and self.project.project_name:
            return '%s: %s estimate' % (self.project.project_name, self.date)
        else:
            return 'unnamed'

class Production(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    date = ApproximateDateField(blank=True,null=True)
    commodity = models.CharField(max_length=100,
                                 choices=COMMODITIES)
    actual_predicted = models.CharField(max_length=10,
                                        choices=(
                                            ('actual', 'Actual'),
                                            ('predicted', 'Predicted'),))
    confidence = models.CharField(max_length=20,
                                  choices=CONFIDENCE_MEASURES,
                                  null=True,
                                  blank=True)
    level = models.FloatField()
    unit = models.CharField(
        max_length=20,
        choices = UNITS,
        default = 'mbbls')
    per = models.CharField(
        max_length=20,
        choices=TIME_PERIODS,
        default='year')

    source = models.ForeignKey(Document, blank=True, null=True)
    

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
    
