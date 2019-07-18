from egl_rest.api.helpers import Singleton


class FederationData(Singleton):
    supported_schemas = [1.0]

    def __init__(self):
        Singleton.__init__(self)

    @staticmethod
    def get_latest_schema():
        FederationData.supported_schemas.sort()
        return FederationData.supported_schemas[-1]


    @staticmethod
    def render(federation, version):
        if version == 1.0:
            return FederationData.generate_v1_0(federation)
        else:
            raise Exception("Schema version {version} not supported for sites.".format(version=version))

    @staticmethod
    def generate_v1_0(federation):
        supported_vos = []
        sites = []
        pledges = {}
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

            pledges[pledge.vo.name] = {
                pledge.year: {
                    "cpu": cpu,
                    "disk": disk,
                    "tape": tape
                }
            }
        federation_dict = {
            "name": federation.name,
            "accounting_name": federation.accounting_name,
            "tier": federation.tier,
            "supported_vos": supported_vos,
            "sites": sites,
            "pledges": pledges
        }
        return federation_dict
