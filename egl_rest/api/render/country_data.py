from egl_rest.api.services.site_service import SiteService
from egl_rest.api.helpers import get_py_country


class CountryData:
    supported_schemas = [1.0]

    @staticmethod
    def get_latest_schema():
        CountryData.supported_schemas.sort()
        return CountryData.supported_schemas[-1]

    @staticmethod
    def render(country, version):
        if version == 1.0:
            return CountryData.generate_v1_0(country)
        else:
            raise Exception("Schema version {version} not supported for countries.".format(version=version))

    @staticmethod
    def generate_v1_0(country):
        sites = []
        country_code = None
        for site in SiteService.get_active_sites().filter(country=country):
            sites.append(site.name)
            country_code = site.country_code
        pycountry = get_py_country(country)
        if pycountry is not None:
            country_code = pycountry.alpha_2
        country_dict = {
            "country": country,
            "country_code": country_code,
            "sites": sites
        }
        return country_dict
