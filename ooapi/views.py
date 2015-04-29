from django.shortcuts import render
from ooapi.models import Concession

from django.http import JsonResponse
# Create your views here.

def concessions(request):
    query = Concession.objects.all()
    if 'country' in request.GET:
        query = query.filter(country=request.GET['country'])

    # offset/limit

    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 100))
    index_start = (page-1) * per_page
    index_end = index_start + per_page
        
    query = query[index_start:index_end]

    results = concs_as_dicts(query)

    output = {
        'api_version': 0.1,
        'result_count': query.count(),
        'page': page,
        'per_page': per_page,
        'results': results
    }
    
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
