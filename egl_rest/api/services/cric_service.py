from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.event_managers import IEGLEventListener
from egl_rest.api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
from egl_rest.api.helpers import Singleton
from egl_rest.api.recon_chewbacca import ReconChewbacca


class CRICService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)

    def notify(self, egl_event):
        if egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "cric_federations":
            self.process_cric_federations(egl_event.data['data'])
        elif egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "cric_sites":
            self.process_cric_sites(egl_event.data['data'])

    def process_cric_sites(self, cric_sites_file):
        pass

    def process_cric_federations(self, cric_federations_file):
        pass
