from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.event_managers import IEGLEventListener
from egl_rest.api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
from egl_rest.api.helpers import Singleton
from egl_rest.api.recon_chewbacca import ReconChewbacca
import json
from egl_rest.api.models import Federation, Pledge, VO
from egl_rest.api.services.federations_service import FederationsService
from egl_rest.api.services.pledge_service import PledgeService
from egl_rest.api.services.vo_service import VOService


class CRICService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)

    def notify(self, egl_event):
        if egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "cric_federations":
            self.process_cric_federations(egl_event.data['data'])
        elif egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "cric_sites":
            self.process_cric_sites(egl_event.data['data'])

    @staticmethod
    def process_cric_sites(cric_sites_file):
        with open(cric_sites_file) as file:
            sites = json.load(file)
            #print(sites)

    @staticmethod
    def process_cric_federations(cric_federations_file):
        with open(cric_federations_file) as file:
            federations = json.load(file)
            for federation_name, federation in federations.items():
                fed_obj = FederationsService.get_or_create(federation_name)
                fed_obj.accounting_name = federation['accounting_name']
                print(fed_obj.accounting_name)
                for vo_name in federation['vos']:
                    vo = VOService.get_or_create(vo_name)
                    fed_obj.supported_vos.add(vo)
                pledges = federation['pledges']
                for year, vos in pledges.items():
                    for vo, pledge in vos.items():
                        vo_obj = VOService.get_or_create(vo)
                        pledge_obj = PledgeService.get_or_create(fed_obj, vo_obj)
                        pledge_obj.year = year
                        if 'CPU' in pledge:
                            pledge_obj.cpu = pledge['CPU']
                        if 'Disk' in pledge:
                            pledge_obj.disk = pledge['Disk']
                        if 'Tape' in pledge:
                            pledge_obj.tape = pledge['Tape']
                        fed_obj.pledge_set.add(pledge_obj)
                FederationsService.save(fed_obj)
