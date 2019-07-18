from egl_rest.api.render.country_data import CountryData
from egl_rest.api.services.site_service import SiteService
import json

class CountryService:
    @staticmethod
    def get_all():
        active_sites = SiteService.get_active_sites()
        countries = []
        for site in active_sites:
            countries.append(site.country)
        return countries

    @staticmethod
    def generate_country_data(countries, version):
        if version not in CountryData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=CountryData.supported_schemas
            )
        output = {'countries': [], 'meta': [], 'current_schema_version': version,
                  'latest_schema_version': CountryData.get_latest_schema()}
        for country in countries:
            output['countries'].append(CountryData.render(country,version))
        output['meta'] = CountryService.analyse(countries)
        return json.dumps(output)

    @staticmethod
    def analyse(countries):
        return {
            "count": len(countries)
        }
