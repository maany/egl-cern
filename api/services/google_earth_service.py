from api.event_hub.event_managers import IEGLEventListener
from api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent

class GoogleEarthService(IEGLEventListener):

    def __init__(self):
        
    @classmethod
    def process_kml(cls):
        pass

    def notify(self, egl_event):
        if egl_event.sequence contain
