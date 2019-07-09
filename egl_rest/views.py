from django.db.models import QuerySet, Q
from django.http import HttpResponse, Http404
import json

from egl_rest.api.models import Site
from egl_rest.api.render.site_data import SiteData
from egl_rest.api.render.vo_data import VOData
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.vo_service import VOService

# Create your views here.
def sites(request):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = SiteData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    filters = {
        'name': request.GET.get('name'),
        'tier': request.GET.get('tier'),
        'sitevo__vo__name__in': request.GET.get('supported_vos').split(','),
        'country': request.GET.get('country'),
        'country_code': request.GET.get('country_code'),
        'federation': request.GET.get('federation')
    }

    trimmed_filters = {}
    for key, val in filters.items():
        if val is not None:
            trimmed_filters[key] = val

    filtered_sites = SiteService.get_all()
    filtered_sites = filtered_sites.complex_filter(trimmed_filters)
    output = SiteService.generate_site_data(filtered_sites, schema_version)
    return HttpResponse(output)


def site(request, site_id):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = SiteData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    try:
        the_site = SiteService.get_by_id(site_id)
    except Site.DoesNotExist:
        raise Http404("Site does not exist!")
    output = SiteService.generate_site_data(the_site, schema_version)
    return HttpResponse(output)


def vos(request):
    vos = VOService.get_all()
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = SiteData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    output = VOService.generate_vo_data(vos,schema_version)
    return HttpResponse(output)


def data_links(request):
    all_links = []
    return HttpResponse(json.dumps(all_links))
