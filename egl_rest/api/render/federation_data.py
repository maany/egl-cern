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
            pledges = []
            for vo in federation.supported_vos.all():
                supported_vos.append(vo.name)
            for site in federation.site_set.filter(active=True):
                sites.append(site.name)
            for pledge in federation.pledge_set.all():
                if pledge.tape is -1:
                    tape = "Not Specified"
                else:
                    tape = pledge.tape
                if pledge.cpu is -1:
                    cpu = "Not Specified"
                else:
                    cpu = pledge.cpu
                if pledge.disk is -1:
                    disk = "Not Specified"
                else:
                    disk = pledge.disk

                pledges.append({
                    pledge.year: {
                        "cpu": cpu,
                        "disk": disk,
                        "tape": tape
                    }
                })
            federations_dict[federation.name] = {
                "accounting_name": federation.accounting_name,
                "supported_vos": supported_vos,
                "sites": sites,
                "pledges": pledges
            }
        json_rep = json.dumps(federations_dict)
        return json_rep
