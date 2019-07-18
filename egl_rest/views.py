from django.http import HttpResponse, Http404
import json

from egl_rest.api.models import Site, VO, Federation
from egl_rest.api.render.country_data import CountryData
from egl_rest.api.render.federation_data import FederationData
from egl_rest.api.render.site_data import SiteData
from egl_rest.api.render.transfer_data import TransferData
from egl_rest.api.render.vo_data import VOData
from egl_rest.api.services.country_service import CountryService
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.services.site_service import SiteService
from egl_rest.api.services.transfers_service import TransfersService
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

    filtered_sites = SiteService.get_active_sites()
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
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = TransferData.get_latest_schema()
    else:
        schema_version = float(schema_version)
    filters = {
        "source": request.GET.get('source'),
        "destination": request.GET.get('destination'),
        "vo": request.GET.get('vo'),
        "technology": request.GET.get('technology'),
        "starts_between": request.GET.get('starts_between'),
        "ends_between": request.GET.get('ends_between'),
        "minimum_transferred_volume": request.GET.get('minimum_transferred_volume'),
        "maximum_transferred_volume": request.GET.get('maximum_transferred_volume'),
        "limit": request.GET.get('limit')
    }

    trimmed_filters = {}
    for key, val in filters.items():
        if val is not None:
            trimmed_filters[key] = val
    if "starts_between" not in trimmed_filters.keys() and "ends_between" not in trimmed_filters.keys():
        raise Http404("Please specify the filter 'starts_between' or 'ends_between'")
    filtered_transfers = TransfersService.fetch_transfers(trimmed_filters)
    output = TransfersService.generate_transfer_data(filtered_transfers, schema_version)
    return HttpResponse(output)


def raw_data_links(request):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = TransferData.get_latest_schema()
    else:
        schema_version = float(schema_version)
    filters = {
        "source": request.GET.get('source'),
        "destination": request.GET.get('destination'),
        "vo": request.GET.get('vo'),
        "technology": request.GET.get('technology'),
        "starts_between": request.GET.get('starts_between'),
        "ends_between": request.GET.get('ends_between'),
        "minimum_transferred_volume": request.GET.get('minimum_transferred_volume'),
        "maximum_transferred_volume": request.GET.get('maximum_transferred_volume'),
        "limit": request.GET.get('limit')
    }

    trimmed_filters = {}
    for key, val in filters.items():
        if val is not None:
            trimmed_filters[key] = val
    if "starts_between" not in trimmed_filters.keys() and "ends_between" not in trimmed_filters.keys():
        raise Http404("Please specify the filter 'starts_between' or 'ends_between'")
    filtered_transfers = TransfersService.fetch_raw_transfers(trimmed_filters)
    output = TransfersService.generate_raw_transfer_data(filtered_transfers, schema_version)
    return HttpResponse(output)


def countries(request):
    schema_version = request.GET.get('schema_version')
    if schema_version is None:
        schema_version = CountryData.get_latest_schema()
    else:
        schema_version = float(schema_version)
    countries = CountryService.get_all()
    output = CountryService.generate_country_data(countries, schema_version)
    return HttpResponse(output)