from django.shortcuts import render
from django import forms
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from modeling import models

import csv
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
    
    return render(request, "import_csv.html", {
        'form': form,
    })


def make_modelform(klass):
    class KlassForm(forms.ModelForm):
        class Meta:
            model = klass
            exclude = []
    return KlassForm
    
        
@login_required()
def import_manual(request):
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
    formset = formset_factory(make_modelform(klass), extra=10)
    return render(request, "import_manual.jinja", {
        'formset': formset,
        'tabledata': json.dumps(tabledata),
        'autocomplete_projects': json.dumps(autocomplete_projects),
        'autocomplete_companies': json.dumps(autocomplete_companies),
        'autocomplete_otherfields': json.dumps(autocomplete_fields),
                                                   })


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
        import pprint
        pprint.pprint(tabledata)
        pprint.pprint(metadata)
    else:
        print('not even a post')
    return HttpResponse('OK')
