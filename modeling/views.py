from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django_date_extensions.fields import ApproximateDateFormField
#from datetimewidget.widgets import DateTimeWidget
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
    'reserves': models.Reserve,
    'costs': models.Cost,
    'extra_information': models.ExtraInformation}

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


def add_row(line, klass, standard_cols):
        if klass in MODELCLASSES.keys():
            modelclass = MODELCLASSES[klass]

            if 'project' in line:
                project, created = models.Project.objects.get_or_create(
                    project_name = line.pop('project'),
                    defaults = {'type': 'project'},)
                line['project'] = project

            try:
                rawdate = line.pop('date')
                line['date'] = ApproximateDateFormField().clean(rawdate)
                
            except (ValueError,   # badly-formatted date
                    KeyError):    # no date
                print(
                    'could not make sense of date')
                date = None
                
            if klass in ('production', 'reserves', 'extra_information'):
                if 'company' in line:
                    company, created = models.Company.objects.get_or_create(
                        company_name = line.pop('company'))
                    line['company'] = company
            extra_data = {}
            for k in line.keys():
                if k not in standard_cols:
                    extra_data[k] = line.pop(k)
                    
            newrow = modelclass(
                extra_data = extra_data,
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
            process_csv(request.FILES['file'], form.cleaned_data['category'])
            return HttpResponse('OK')
        else:
            pass


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
    #publish_date = forms.CharField(
    #    required=False,
    #    label="When was the document published",
    #    widget=DateTimeWidget()
    #),
    pagenum = forms.CharField(label="what pages of the PDF do you want data from?")

    publish_date= forms.DateField(
        label="When was the document published?",
        widget = forms.DateInput(),
    )

    # set up the greyed-out text
    placeholders = {
        doc_description: 'try to be unique!',
        doc_url: 'http://example.com/dir/file.pdf',
        pagenum: '1,3,4-8',
    }
    for (k,v) in placeholders.items():
        k.widget = forms.TextInput(
            attrs = {'placeholder': v,
                     'size': "100"})

    del(k) # otherwise, Django will interpret this as another field to add
    

def process_new_document(form):
    # create a Document instance
    doc = models.Document(
        source_url = form.cleaned_data['doc_url'],
        description = form.cleaned_data['doc_description'],
        publish_date= form.cleaned_data['publish_date'].strftime('%F'),
    )
    doc.save()

    metadata = {
        'uploaded_date': datetime.datetime.now().strftime('%F'),
        'import_method': 'web upload form',
        'source_pagenum': form.cleaned_data['pagenum'],
        }
    pagenums = pdftables.interpret_range(form.cleaned_data['pagenum'])
    pdfurl = form.cleaned_data['doc_url']
    fullfile = pdftables.dl_pdf(pdfurl)
    edatas = []
    for pagenum in pagenums:
        fn_page = pdftables.page_from_pdf(fullfile.name, pagenum)
        result = pdftables.tables_from_page(fn_page)
        as_json = pdftables.csv_to_json(result)
        edata = models.ExtractedData(
            metadata = metadata,
            document = doc,
            data = as_json)
        edata.save()
        edatas.append(edata)
    return(edatas)


    # send the page through PDFtables
    #csvblob = pdftables.page_to_csv(form.cleaned_data['doc_url'], form.cleaned_data['pagenum'])
    #as_json = pdftables.csv_to_json(csvblob)

    # compile results into the database
    # return ExtractedData
    #return edata
    
@login_required()
def import_pdf(request):
    if request.method == 'POST':
        form = ImportPDFForm(request.POST, request.FILES)
        if form.is_valid():
            edatas = process_new_document(form)
            messages.add_message(request, messages.INFO, "Added %s pages to review queue" % len(edatas))
            step2_url = '/data/add/manual?edata=%s' % (edatas[0].id)
            return HttpResponseRedirect(step2_url) # redirect to the form
        else:
            pass

    else:
        form = ImportPDFForm()

    return render(request, "import_pdf.jinja", {
            'form': form,
        })

def get_columns(modelname):
    klass = MODELCLASSES.get(modelname, models.Production)
    modelform = make_modelform(klass)
    columns = [x.title() for x in modelform.base_fields.keys()]
    columns.pop(columns.index('Extra_Data'))
    return columns
    

def build_empty_table_json(modelname):
    columns = get_columns(modelname)

    klass = MODELCLASSES.get(modelname, models.Production)
    modelform = make_modelform(klass)
    
    tabledata = [columns]
    for i in range(5):
        tabledata.append([''] * len(columns))

    # autocomplete for all the choice fields
    # (using the django forms infrastructure for some preprocessing
    autocomplete_fields = dict((x,list(z[0] for z in y.choices))
                               for (x,y) in modelform.base_fields.items()
                               if hasattr(y, 'choices')
                               and x not in (
                                   'company', 'project', #handled separately
                                   'source_document', #not yet implemented
                                   'extra_data', #done with manually-added columns
                               ))

    return json.dumps(tabledata), json.dumps(autocomplete_fields)


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

    

    autocomplete_companies = [x.company_name for x in models.Company.objects.all()]
    autocomplete_projects = [x.project_name for x in models.Project.objects.all()]

    
    templatedata = {
        # output table         
        'autocomplete_projects': json.dumps(autocomplete_projects),
        'autocomplete_companies': json.dumps(autocomplete_companies),
    }

    for tablename in ('production', 'reserves', 'costs', 'extra_information'):
        jsondata, autocomplete = build_empty_table_json(tablename)
        templatedata['headers_%s' % tablename] = jsondata
        templatedata['autocomplete_%s' % tablename] = autocomplete

    
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
def review_queue(request):
    next_for_review = models.ExtractedData.objects.filter(reviewed=False).first()
    if next_for_review is None:
        messages.add_message(request, messages.INFO, "There are no more data review tasks to complete")
        return HttpResponseRedirect('/data') # redirect to the form
    url = '/data/add/manual?edata=%s' % next_for_review.id
    return HttpResponseRedirect(url) # redirect to the form
    
@login_required()
def import_json(request):
    '''handle uploaded tabular data
    this works with the form at add/manual
    but can also be used directly
    '''
    if request.method == 'POST':
        tabledata = json.loads(request.POST['tabledata'])
        metadata = json.loads(request.POST['metadata'])
        klass = metadata['type']
        cols = [x.lower() for x in tabledata[0] if x]
        standard_cols = [x.lower() for x in get_columns(klass)]

        for row in tabledata[1:]:
            if not any(row):
                break
            labeled_rows = zip(cols,row)
            # treat blank rows as blank -- let the model fill in the defaults
            rowdata = dict(itertools.ifilter(lambda (x,y): y != "", labeled_rows))
            add_row(rowdata, klass, standard_cols)
        mark_data_processed(metadata)
    return HttpResponse('OK')

