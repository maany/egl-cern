from egl_rest.api import EventHub
from egl_rest.api import GoogleEarthService
from egl_rest.api import Singleton

### Service loading and Event Hub loading ###
class EGL(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.event_hub = EventHub()
        self.google_earth_service = GoogleEarthService()
