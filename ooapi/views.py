from django.shortcuts import render
from ooapi.models import Concession

from django.http import JsonResponse
# Create your views here.

def concessions(request):
    query = Concession.objects.all()
    if 'country' in request.GET:
        query = query.filter(country=request.GET['country'])
    output = concs_as_dicts(query)
    return JsonResponse(output, safe=False)

def concs_as_dicts(matches):
    output = []
    for match in matches:
        data = {}
        for field in ('name', 'type'):
            data[field] = getattr(match, field)
        data['country'] = match.country.code
        output.append(data)
    return output
