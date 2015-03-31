from django.shortcuts import render
from modeling import models

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required()
def infotypes(request):
    return render(request, "datatypes.html", {"tabledata": models.InformationType.objects.all()})

@login_required()
def datasources(request):
    return render(request, "datatypes.html", {"tabledata": models.DataSource.objects.all()})

@login_required()
def reserve(request):
    return render(request, "datatypes.html", {"tabledata": models.Reserve.objects.all()})
