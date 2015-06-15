from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from modeling import models
from modeling import pdftables

import csv
import datetime
import io
import json
import dateutil.parser
import itertools

# Create your views here.
from django.contrib.auth.decorators import login_required

MODELCLASSES = {
    'production': models.Production,
    'reserve': models.Reserve,
    'cost': models.Cost}

@login_required()
def dataindex(request):
    return render(request, "dataindex.jinja", {})

@login_required()
def infotypes(request):
    return render(request, "datatypes.html", {"tabledata": models.InformationType.objects.all()})

@login_required()
def datasources(request):
    return render(request, "datatypes.html", {"tabledata": models.DataSource.objects.all()})

@login_required()
def reserves(request):
    return render(request, "datatypes.html", {"tabledata": models.Reserve.objects.all()})

@login_required()
def production(request):
    return render(request, "datatypes.html", {"tabledata": models.Production.objects.all()})


@login_required()
def costs(request):
    return render(request, "datatypes.html", {"tabledata": models.Cost.objects.all()})

class CSVUploadForm(forms.Form):
    category = forms.ChoiceField(
        choices = (
            ('production', 'Production'),
            ('reserves', 'Reserves'),
            ('costs', 'Costs')
               ) )
    file = forms.FileField(required=True)

    
def process_csv(csvfile, klass):
    stringfile = io.StringIO(csvfile.read().decode(encoding="UTF-8"))
    reader = csv.DictReader(stringfile)
    for line in reader:
        add_row(line,klass)


def add_row(line, klass):        
        modelclass = MODELCLASSES[klass]
        if klass in ('production', 'reserve', 'cost'):
            project, created = models.Project.objects.get_or_create(
                project_name = line.pop('project'), defaults = {'type': 'project'},
                )
            date = dateutil.parser.parse(line.pop('date')).strftime('%Y-%m-%d')
            if klass in ('production', 'reserve'):
                company, created = models.Company.objects.get_or_create(
                    company_name = line.pop('company'))
                line['company'] = company
            print(modelclass, line)
            newrow = modelclass(
                project = project,
                date=date,
                **line)
            newrow.save()
            # XXX add sourcing info here

def process_table(tabledata, klass):
    pass
            
@login_required()
def import_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print('form OK') # XXX writeme
            process_csv(request.FILES['file'], form.cleaned_data['category'])
            return HttpResponse('OK')
        else:
            print('form not OK')

    else:
        form = CSVUploadForm()
    
    return render(request, "import_csv.jinja", {
        'form': form,
    })


def make_modelform(klass):
    class KlassForm(forms.ModelForm):
        class Meta:
            model = klass
            exclude = ['source',]
    return KlassForm


class ImportPDFForm(forms.Form):
    doc_description = forms.CharField(label="description of the source", max_length=100)
    doc_url = forms.URLField(label="where is the PDF?")
    pagenum = forms.IntegerField(label="what page of the PDF do you want data from?")
    information_type = forms.ChoiceField(
        label = 'What kind of information is on this page?',
        choices = (
            ('production', 'Production'),
            ('reserves', 'Reserves'),
            ('costs', 'Costs')
               ) )

def process_new_document(form):
    # create a Document instance
    doc = models.Document(
        source_url = form.cleaned_data['doc_url'],
        description = form.cleaned_data['doc_description'])
    doc.save()

    metadata = {
        'uploaded_date': datetime.datetime.now().strftime('%F'),
        'import_method': 'web upload form',
        'source_pagenum': form.cleaned_data['pagenum'],
        'information_type': form.cleaned_data['information_type'],
        }
    
    # send the page through PDFtables
    csvblob = pdftables.page_to_csv(form.cleaned_data['doc_url'], form.cleaned_data['pagenum'])
    as_json = pdftables.csv_to_json(csvblob)

    # compile results into the database
    edata = models.ExtractedData(
        metadata = metadata,
        document = doc,
        data = as_json)
    edata.save()
    # return ExtractedData
    return edata
    
@login_required()
def import_pdf(request):
    if request.method == 'POST':
        form = ImportPDFForm(request.POST, request.FILES)
        if form.is_valid():
            print('form OK') # XXX writeme
            edata = process_new_document(form)
            step2_url = '/data/add/manual?edata=%s&type=%s' % (edata.id, edata.metadata['information_type'])
            return HttpResponseRedirect(step2_url) # redirect to the form
        else:
            pass

    else:
        form = ImportPDFForm()

    return render(request, "import_pdf.jinja", {
            'form': form,
        })


@login_required()
def import_manual(request):

    # Extracted data
    edata_id = request.GET.get('edata', None)
    edata = None
    if edata_id:
        try:
            edata = models.ExtractedData.objects.get(pk=edata_id)
        except (ValueError, models.ExtractedData.DoesNotExist):
            pass
        # grab edata by ID (access checks here!)

    # Output table
    modelname = request.GET.get('type', 'production')
    klass = MODELCLASSES.get(modelname, models.Production)
    modelform = make_modelform(klass)
    columns = [x.title() for x in modelform.base_fields.keys()]

    # autocomplete for all the choice fields
    # (using the django forms infrastructure for some preprocessing
    autocomplete_fields = dict((x,list(z[0] for z in y.choices))
                               for (x,y) in modelform.base_fields.items()
                               if hasattr(y, 'choices')
                               and x not in (
                                   'company', 'project', #handled separately
                                   'source_document', #not yet implemented
                               ))
                                
    tabledata = [columns]
    autocomplete_companies = [x.company_name for x in models.Company.objects.all()]
    autocomplete_projects = [x.project_name for x in models.Project.objects.all()]
    for i in range(5):
        tabledata.append([''] * len(columns))
    #formset = formset_factory(make_modelform(klass), extra=10)

    templatedata = {
        #'formset': formset,
        # output table 
        'tabledata': json.dumps(tabledata),
        'autocomplete_projects': json.dumps(autocomplete_projects),
        'autocomplete_companies': json.dumps(autocomplete_companies),
        'autocomplete_otherfields': json.dumps(autocomplete_fields),
                                                   }
    if edata:
        templatedata['edata_json'] = json.dumps(edata.data)
        templatedata['edata_obj'] = edata
    else:
        templatedata['edata_json'] = json.dumps({})
        templatedata['edata_obj'] = ''
    return render(request, "import_manual.jinja", templatedata)

def mark_data_processed(metadata):
    '''
    if this data is associated with an ExtractedData object, mark the latter
    as reviewed
    '''
    edata_id = metadata.get('edata_id', None)
    try:
        edata = models.ExtractedData.objects.get(pk=edata_id)
    except (ValueError, models.ExtractedData.DoesNotExist):
        return
    edata.reviewed = True
    edata.save()
    return

    
@login_required()
def import_json(request):
    '''handle uploaded tabular data
    this works with the form at add/manual
    but can also be used directly
    '''
    if request.method == 'POST':
        tabledata = json.loads(request.POST['tabledata'])
        metadata = json.loads(request.POST['metadata'])
        klass = 'production' #XXX writme!
        cols = [x.lower() for x in tabledata[0]]

        for row in tabledata[1:]:
            if not any(row):
                break
            labeled_rows = zip(cols,row)
            # treat blank rows as blank -- let the model fill in the defaults
            rowdata = dict(itertools.ifilter(lambda (x,y): y, labeled_rows))
            print(rowdata)
            add_row(rowdata, klass)
        mark_data_processed(metadata)
    else:
        print('not even a post')
    return HttpResponseRedirect('/data') # redirect to the form
