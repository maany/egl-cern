from api.event_hub.event_managers import IEGLEventListener
from api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
from api.event_hub import EventHub
from api.helpers import Singleton
from api.recon_chewbacca import ReconChewbacca

class GoogleEarthService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)

    def process_kml(self, google_earth_data_holder):
        print("Processing KML")
        with open(google_earth_data_holder, 'r') as file:
            print(file.readlines())

    def notify(self, egl_event):
        if egl_event.created_by is ReconChewbacca.__name__ and egl_event.data['source'] is "google_earth":
            self.process_kml(egl_event.data['data'])
