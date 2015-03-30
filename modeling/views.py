from django.shortcuts import render
from modeling import models

# Create your views here.

def sources(request):
    return render(request, "datatypes.html", {"datatypes": models.InformationType.objects.all()})
