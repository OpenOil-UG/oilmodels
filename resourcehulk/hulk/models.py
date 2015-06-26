from django_pg import models
from datetime import datetime
from django_countries.fields import CountryField
from django_date_extensions.fields import ApproximateDateField
import uuid

def random_id(*args, **kwargs):
    return uuid.uuid4().hex

class Project(models.Model):
    project_id = models.CharField(primary_key=True, max_length=200, default=random_id)    
    project_name = models.CharField(max_length=200,null=True,blank=True)
    type = models.CharField(max_length=100,
                                       choices = (
                                           ('well', 'Well'),
                                           ('field', 'Field'),
                                           ('project', 'Project'),
                                           ('company-country', 'Company (all operations in one country)'),
                                       ))

    country = CountryField(blank=True,null=True)
    source = models.ForeignKey('SourceInfo', null=True,blank=True)
    parent = models.ForeignKey('Project', null=True, blank=True, related_name="subprojects")


    def __str__(self):
        return self.project_name or '<untitled>'

class Company(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200, default=random_id)
    company_name = models.CharField(max_length=200)
    
    cik = models.IntegerField(blank=True, null=True, db_index=True)
    sic = models.IntegerField(blank=True, null=True)
    jurisdiction = models.CharField(max_length=50, blank=True)

    source=models.ForeignKey('SourceInfo', blank=True,null=True, related_name='companies')

    class Meta:
        ordering = ['company_name',]

    def __str__(self):
        return self.company_name or '<untitled>'


class Document(models.Model):
    doc_id = models.CharField(primary_key=True, max_length=200, default=random_id)
    description  = models.CharField(blank=True,null=True,max_length=300)
    source_url = models.CharField(max_length=200, default='') # original source
    mirror_url = models.CharField(max_length=200, default='') #

    publish_date = ApproximateDateField(blank=True,null=True,
                               help_text = "When the document was published")

    import_date = models.DateTimeField(auto_now_add=True)
    
    # source is left here to avoid breaking ResourceHulk,
    # but is no longer really in use
    source = models.ForeignKey('SourceInfo', null=True,blank=True)


    metadata = models.JSONField(null=True,blank=True)
    # metadata we might be interested in:
    #  file type
    #  size    
    
    def __str__(self):
        return self.source_url or '<untitled>'



    
class SourceInfo(models.Model):
    '''
    Contains source information
    '''
    id = models.AutoField(primary_key=True)
    contributor = models.CharField(max_length=200)
    license = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)
    info = models.JSONField(type=dict, default={})

    def __str__(self):
        return '%s under %s license' % (self.contributor, self.license)

class Search(models.Model):
    '''
    Represents one run of any of the data-searching code
    '''
    label = models.CharField(max_length=10, primary_key=True)
    metadata = models.JSONField(type=dict)
    source = models.ForeignKey('SourceInfo', null=True,blank=True)

    def __str__(self):
        return self.label or '<untitled>'


class SearchResult(models.Model):
    id = models.AutoField(primary_key=True)
    search = models.ForeignKey('Search', related_name='results')
    sequencenum = models.IntegerField()
    metadata = models.JSONField(type=dict)

    def __str__(self):
        return self.metadata.get('extract', str(self.sequencenum))





class ConcessionAlias(models.Model):
    concession_alias = models.CharField(primary_key=True, max_length=200)
    concession_id = models.CharField(max_length=200)


    def __str__(self):
        return self.concession_alias or '<untitled>'


class Concession(models.Model):
    concession_id = models.CharField(primary_key=True, max_length=200)
    concession_name = models.CharField(max_length=200)
    unep_geo_id = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200)
    source = models.ForeignKey('SourceInfo', null=True,blank=True)


    def __str__(self):
        return self.concession_name or '<untitled>'



class Contract(models.Model):
    contract_id = models.CharField(primary_key=True, max_length=200)
    doc = models.ForeignKey('Document',null=True,blank=True)
    country = models.CharField(max_length=200)
    sign_date = models.CharField(max_length=200)
    title_type = models.CharField(max_length=200, blank=True)
    source_url = models.CharField(max_length=200)
    doc_cloud_id = models.CharField(max_length=200)
    doc_cloud_url = models.CharField(max_length=200)
    sign_year = models.CharField(max_length=200)
    source = models.ForeignKey('SourceInfo', null=True,blank=True)


    def __str__(self):
        return self.contract_id or '<untitled>'


class Statement(models.Model):
    statement_id = models.CharField(primary_key=True, max_length=200, default=random_id)
    doc = models.ForeignKey(Document,blank=True,null=True,default=None)
    statement_content = models.CharField(max_length=200)
    definitive = models.BooleanField(default=False)

    projects = models.ManyToManyField('Project', blank=True)
    companies = models.ManyToManyField('Company', blank=True)
    concessions = models.ManyToManyField('Concession',
                                         blank=True)
    contracts = models.ManyToManyField('Contract', 
                                      blank=True)

    source = models.ForeignKey('SourceInfo', null=True,blank=True)



    def __str__(self):
        return self.statement_content or '<untitled>'
