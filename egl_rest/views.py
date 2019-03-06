from django.shortcuts import render
from django.http import HttpResponse
import requests

cms_cric_url = "https://cms-cric.cern.ch/api/core/rcsite/query/?json"
wlcg_cric_url = "https://wlcg-cric.cern.ch/api/core/rcsite/query/?json"

# Create your views here.
def index(request):
    output = requests.get(cms_cric_url, verify = False)
    return HttpResponse(output.text)
