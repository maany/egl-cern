from api.event_hub.event_managers import IEGLEventListener
from api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
from api.event_hub import EventHub


class GoogleEarthService(IEGLEventListener):

    def __init__(self):
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)

    def process_kml(self):
        print("Processing KML")

    def notify(self, egl_event):
        self.process_kml()
