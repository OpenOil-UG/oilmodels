from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from modeling import models

import csv
import io
import dateutil.parser

# Create your views here.
from django.contrib.auth.decorators import login_required

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
        modelclass = {
            'production': models.Production,
            'reserve': models.Reserve,
            'cost': models.Cost}[klass]
        if klass == 'production':
            print(line)
            project, created = models.Project.objects.get_or_create(
                project_name = line.pop('project'), defaults = {'type': 'project'},
                )
            date = dateutil.parser.parse(line.pop('date')).strftime('%Y-%m-%d')
            if klass in ('production', 'reserve'):
                company, created = models.Company.objects.get_or_create(
                    company_name = line.pop('company'))
                line['company'] = company
            newrow = modelclass(
                project = project,
                date=date,
                **line)
            newrow.save()
            # XXX add sourcing info here

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
