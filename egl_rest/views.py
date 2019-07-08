from django.http import HttpResponse
import json
import xml.etree.ElementTree as ET
from egl_rest.api.services.site_service import SiteService


# Create your views here.
def sites(request):
    output = SiteService.generate_site_data(1.0)
    return HttpResponse(output)


def data_links(request):
    all_links = []
    return HttpResponse(json.dumps(all_links))
