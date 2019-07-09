from egl_rest.api.helpers import Singleton
from egl_rest.api.models import Federation
from egl_rest.api.render.federation_data import FederationData
import json


class FederationsService(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def get_or_create(federation_name):
        return Federation.objects.get_or_create(
            name=federation_name
        )[0]

    @staticmethod
    def get(federation_name):
        return Federation.objects.get(name=federation_name) @staticmethod

    @staticmethod
    def get_by_id(id):
        return Federation.objects.filter(id=id)

    @staticmethod
    def get_all():
        return Federation.objects.all()

    @staticmethod
    def get_all():
        return Federation.objects.all()

    @staticmethod
    def save(federation):
        return federation.save()

    @staticmethod
    def generate_federation_data(federations, version):
        if version not in FederationData.supported_schemas:
            return "Schema version {version} is not supported. Try one of {supported_schemas}".format(
                version=version,
                supported_schemas=FederationData.supported_schemas
            )
        output = {'federations': {}, 'meta': [], 'current_schema_version': version,
                  'latest_schema_version': FederationData.get_latest_schema()}
        for federation in federations:
            output['federations'][federation.name] = FederationData.render(federation, version)
        output['meta'] = FederationsService.analyse(federations)
        return json.dumps(output)

    @staticmethod
    def analyse(federations):
        return {
            'count': len(federations),
            "tier_0_federations": len(federations.filter(tier=0)),
            "tier_1_federations": len(federations.filter(tier=1)),
            "tier_2_federations": len(federations.filter(tier=2))
        }
    @staticmethod
    def get_sites(federation):
        return federation.site_set.all()

