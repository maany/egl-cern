import requests
from requests.exceptions import HTTPError
import logging
import os
from egl_rest.api.helpers import md5_string
from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent
import datetime

# Get instance of logger
logger = logging.getLogger(__name__)


class ReconChewbacca:

    instance = None

    class __ReconChewbacca:
        def __init__(self):
            self.google_earth_kml = "./data/google_earth.xml"
            self.kml_url = "http://dashb-earth.cern.ch/dashboard/dashb-earth-all.kml"
            self.cric_base_url = "http://wlcg-cric.cern.ch/"
            self.cric_federations_url = "{cric_base_url}/api/core/federation/query/?json".format(cric_base_url=self.cric_base_url)
            self.cric_sites_url = "{cric_base_url}/api/core/rcsite/query/?json".format(cric_base_url=self.cric_base_url)
            self.cric_federations_file = "./data/cric_federations.json"
            self.cric_sites_file = "./data/cric_sites.json"
            self.rebus_sites_url = "http://wlcg-rebus.cern.ch/apps/capacities/sites/ALL/{year}/{month}/json".format(year=datetime.datetime.now().year, month=datetime.datetime.now().month)
            self.rebus_sites_file = "./data/rebus_sites.json"

        def hunt_for_updates(self):
            output = {}
            data = {
                'cric_federations': self.cric_federations_file,
                'google_earth': self.google_earth_kml,
                'cric_sites': self.cric_sites_file,
                'rebus_sites': self.rebus_sites_file
            }
            was_kml_updated, kml_message = self.update_google_earth_kml()
            if not was_kml_updated:
                logger.error(kml_message)
            else:
                logger.info(kml_message)

            output['kml_message'] = kml_message

            was_cric_federation_updated, cric_federation_message = self.update_cric_federations_file()
            if not was_cric_federation_updated:
                logger.error(cric_federation_message)
            else:
                logger.info(kml_message)

            output['cric_federations_message'] = cric_federation_message

            was_cric_sites_updated, cric_sites_message = self.update_cric_sites_file()
            if not was_cric_sites_updated:
                logger .error(cric_sites_message)
            else:
                logger.info(cric_sites_message)

            output['cric_sites_message'] = cric_sites_message

            was_rebus_sites_updated, rebus_sites_message = self.update_rebus_sites_file()
            if not was_rebus_sites_updated:
                logger.error(rebus_sites_message)
            else:
                logger.info(rebus_sites_message)

            output['rebus_sites_message'] = rebus_sites_message

            if was_rebus_sites_updated or was_cric_sites_updated or was_cric_federation_updated or was_kml_updated:
                EventHub.announce_event(NewDataAvailableOnlineEvent(
                    created_by=ReconChewbacca.__name__,
                    holder=data
                ))
            return output

        def update_google_earth_kml(self):
            return self.sync_file(self.kml_url, self.google_earth_kml, ssl=True)

        def update_cric_federations_file(self):
            return self.sync_file(self.cric_federations_url, self.cric_federations_file, ssl=True)

        def update_cric_sites_file(self):
            return self.sync_file(self.cric_sites_url, self.cric_sites_file, ssl=True)

        def update_rebus_sites_file(self):
            return self.sync_file(self.rebus_sites_url, self.rebus_sites_file, ssl=False)

        def global_stats_alice_jobs(self):
            pass

        def sync_file(self, url, file, ssl):
            try:
                response = requests.get(url, verify=ssl)
            except HTTPError as http_err:
                message = "Error occurred while fetching {url} : {err}".format(url=url, err=http_err)
                return False, message
            except Exception as err:
                message = "Error occurred while fetching {url} : {err}".format(url=url, err=err)
                return False, message
            new_string = response.text
            file_exists = os.path.isfile(file)
            if not file_exists:
                message = "Saved {file} for the first time"
                with open(file, 'w') as f:
                    f.write(new_string)
                return True, message
            else:
                with open(file, 'r') as f:
                    old_string = f.read()
                    old_hash = md5_string(old_string)
                    new_hash = md5_string(new_string)
                    if old_hash == new_hash:
                        message = "The hash values for old and new data for {file} match. Therefore, " \
                                  "the file was not updated.".format(file=file)
                        return False, message
                with open(file, 'w') as f:
                    message = "The file {file} was updated!".format(file=file)
                    f.write(new_string)
                    return True, message

    def __init__(self):
        if not ReconChewbacca.instance:
            ReconChewbacca.instance = ReconChewbacca.__ReconChewbacca()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)




