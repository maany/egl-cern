from api.event_hub import EventHub
from api.services.google_earth_service import GoogleEarthService
from api.helpers import Singleton

### Service loading and Event Hub loading ###
class EGL(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.event_hub = EventHub()
        self.google_earth_service = GoogleEarthService()
