from django.http import HttpResponse, Http404
import json

from egl_rest.api.models import Site, VO, Federation
from egl_rest.api.render.federation_data import FederationData
from egl_rest.api.render.site_data import SiteData
from egl_rest.api.render.vo_data import VOData
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.vo_service import VOService


# Create your views here.
def sites(request):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = SiteData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    supported_vos = request.GET.get('supported_vos')
    if supported_vos is None:
        supported_vos = None
    else:
        supported_vos = supported_vos.split(',')
    filters = {
        'name': request.GET.get('name'),
        'tier': request.GET.get('tier'),
        'sitevo__vo__name__in': supported_vos,
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
        schema_version = VOData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    output = VOService.generate_vo_data(vos,schema_version)
    return HttpResponse(output)


def vo(request, vo_id):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = VOData.get_latest_schema()
    else:
        schema_version = float(schema_version)

    try:
        the_vo = VOService.get_by_id(vo_id)
    except VO.DoesNotExist:
        raise Http404("VO does not exist!")
    output = VOService.generate_vo_data(the_vo, schema_version)
    return HttpResponse(output)


def federations(request):
    all_federations =FederationsService.get_all()
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = FederationData.get_latest_schema()
    else:
        schema_version = float(schema_version)
    output = FederationsService.generate_federation_data(all_federations, schema_version)
    return HttpResponse(output)


def federation(request, federation_id):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = FederationData.get_latest_schema()
    else:
        schema_version = float(schema_version)
    try:
        the_federation = FederationsService.get_by_id(federation_id)
    except Federation.DoesNotExist:
        raise Http404("Federation does not exist!")
    output = FederationsService.generate_federation_data(the_federation, schema_version)
    return HttpResponse(output)


def data_links(request):
    all_links = []
    return HttpResponse(json.dumps(all_links))
