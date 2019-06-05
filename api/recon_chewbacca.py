import requests
from requests.exceptions import HTTPError
import logging
import os
from api.helpers import md5_string
from api.event_hub import EventHub
from api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
import datetime
# Get instance of logger
logger = logging.getLogger(__name__)


class ReconChewbacca:

    instance = None

    class __ReconChewbacca:
        def __init__(self):
            self.google_earth_kml = "google_earth_recon_test_kml_ref.xml"
            self.kml_url = "http://dashb-earth.cern.ch/dashboard/dashb-earth-all.kml"

        def hunt_for_updates(self):
            was_kml_updated, kml_message = self.update_google_earth_kml()
            if not was_kml_updated:
                logger.error(kml_message)
            else:
                logger.info(kml_message)

            if was_kml_updated:
                EventHub.announce_event(NewDataAvailableOnlineEvent(
                    sequence="Google_Earth_{timestamp}".format(timestamp=datetime.datetime.now()),
                    created_by=ReconChewbacca.__name__,
                    holder={
                        "source": "google_earth",
                        "data": self.google_earth_kml
                    }
                ))
            return kml_message

        def update_google_earth_kml(self):
            try:
                kml_response = requests.get(self.kml_url)
            except HTTPError as http_err:
                message = "Error occurred while fetching Google Earth KML: {err}".format(err=http_err)
                return False, message
            except Exception as err:
                message = "Error occurred while fetching Google Earth KML: {err}".format(err=err)
                return False, message
            new_string = kml_response.text

            kml_exists = os.path.isfile(self.google_earth_kml)
            if not kml_exists:
                message = "Saved KML file for the first time."
                with open(self.google_earth_kml, 'w') as file:
                    file.write(new_string)
                return True, message
            else:
                with open(self.google_earth_kml, "r") as file:
                    old_string = file.read()
                    old_hash = md5_string(old_string)
                    new_hash = md5_string(new_string)
                    if old_hash == new_hash:
                        message = "The hash for old and new kml data match. KML file was not updated"
                        return False, message
                with open(self.google_earth_kml, 'w') as file:
                    message = "The google earth kml file was updated!"
                    file.write(new_string)
                    return True, message

    def __init__(self):
        if not ReconChewbacca.instance:
            ReconChewbacca.instance = ReconChewbacca.__ReconChewbacca()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)


if __name__ == "__main__":
    pass
    #hunt_for_updates()



