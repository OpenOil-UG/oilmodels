from django.shortcuts import render
from ooapi.models import Concession,APIKey
from django.core import exceptions
from django.core.mail import send_mail

from django.http import JsonResponse,HttpResponseForbidden,HttpResponse
# Create your views here.


def require_api_key(func):
    def inner(request, *args, **kwargs):
        key = request.GET.get('apikey', None)
        try:
            k = APIKey.objects.get(key=key)
        except exceptions.ObjectDoesNotExist:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return inner

def mail_apikey(apikey):
    message = '''
    Your key for the OpenOil API is %s

    Learn how to use it at http://openoil.net/openoil-api/
    ''' %apikey.key
    send_mail('OpenOil API Key',message, 'daniel.ohuiginn@openoil.net', [apikey.email],fail_silently=False)
    
def new_api_key(request):
    email = request.GET.get('email',None)
    if email is None:
        return render(request, 'apikey.jinja', {})
    apikey = APIKey(email=email)
    apikey.save()
    mail_apikey(apikey)
    return HttpResponse('your key has been mailed to you')


@require_api_key
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

