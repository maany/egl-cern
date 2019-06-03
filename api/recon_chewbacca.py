import requests
from requests.exceptions import HTTPError
import logging
import os
from api.helpers import md5_string


# Get instance of logger
logger = logging.getLogger(__name__)


def hunt_for_updates():
    was_kml_updated, kml_message = update_google_earth_kml()
    if not was_kml_updated:
        logger.error(kml_message)
    else:
        logger.info(kml_message)

    if was_kml_updated:
        notify
def update_google_earth_kml():
    google_earth_kml = "google_earth_kml.xml"
    kml_url = "http://dashb-earth.cern.ch/dashboard/dashb-earth-all.kml"
    try:
        kml_response = requests.get(kml_url)
    except HTTPError as http_err:
        message = "Error occurred while fetching Google Earth KML: {err}".format(err=http_err)
        return False, message
    except Exception as err:
        message = "Error occurred while fetching Google Earth KML: {err}".format(err=err)
        return False, message
    new_string = kml_response.text

    kml_exists = os.path.isfile(google_earth_kml)
    if not kml_exists:
        message = "Saved KML file for the first time."
        with open(google_earth_kml, 'w') as file:
            file.write(new_string)
        return True, message
    else:
        with open(google_earth_kml, "r") as file:
            old_string = file.read()
            old_hash = md5_string(old_string)
            new_hash = md5_string(new_string)
            if old_hash == new_hash:
                message = "The hash for old and new kml data do not match. KML file was not updated"
                return False, message
        with open(google_earth_kml, 'w') as file:
            message = "The google earth kml file was updated!"
            file.write(new_string)
            return True, message


if __name__ == "__main__":
    hunt_for_updates()



