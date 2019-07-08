from egl_rest.api.helpers import Singleton
from egl_rest.api.services.federations_service import FederationsService
import json


class FederationData(Singleton):
    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def generate_v1_0():
        federations = FederationsService.get_all()
        federations_dict = {}
        for federation in federations:
            supported_vos = []
            sites = []
            for vo in federation.supported_vos.all():
                supported_vos.append(vo.name)
            for site in federation.site_set.filter(active=True):
                sites.append(site.name)
            federations_dict[federation.name] = {
                "accounting_name": federation.accounting_name,
                "supported_vos": supported_vos,
                "sites": sites
            }
        json_rep = json.dumps(federations_dict)
        return json_rep
