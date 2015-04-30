from django.shortcuts import render
from ooapi.models import Concession

from django.http import JsonResponse
# Create your views here.

def concessions(request):
    query = Concession.objects.all()
    
    if 'country' in request.GET:
        query = query.filter(country=request.GET['country'])

    if 'type' in request.GET:
        query = query.filter(type=request.GET['type'])

    if 'status' in request.GET:
        query = query.filter(status=request.GET['status'])

        
    # offset/limit

    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 100))
    index_start = (page-1) * per_page
    index_end = index_start + per_page

    resultcount = query.count()
    query = query[index_start:index_end]

    results = concs_as_dicts(query)

    output = {
        'api_version': 0.1,
        'result_count': resultcount,
        'page': page,
        'per_page': per_page,
        'results': results
    }
    
    return JsonResponse(output, safe=False)

def concs_as_dicts(matches):
    output = []
    for conc in matches:
        output.append(conc.infodict())
    return output

def documentation(request):
    return render(request, 'documentation.jinja', {})

