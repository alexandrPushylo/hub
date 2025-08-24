import json

from django.http import HttpResponse
from django.middleware.csrf import get_token

# Create your views here.

from logger import getLogger
log = getLogger(__name__)

# @csrf_protect
def test_api(request):
    get_token(request)
    if request.method == 'GET':
        out = {
            "csrfmiddlewaretoken": get_token(request),
        }
        return HttpResponse(json.dumps(out), content_type='application/json')
    if request.method == 'POST':
        return HttpResponse('post')
    return HttpResponse('none')