from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.events.data_fetch_parse_events import SequenceCompletedEvent
from egl_rest.api.services.cric_service import CRICService
from egl_rest.api.services.rebus_service import RebusService
from enum import Enum

from egl_rest.api.services.site_service import SiteService


class SequenceStatus(Enum):
    INIT = 1
    PARSE_CRIC_FEDERATION = 3
    PARSE_CRIC_SITES = 4
    PARSE_REBUS_SITES = 5
    PROCESS_SITES = 6
    ANALYSE = 7
    END = 8


class Sequence:
    def __init__(self, name, timestamp, data):
        self.name = name
        self.initial_timestamp = timestamp
        self.status = None
        self.data = data
        for source, file_name in data.items():
            self.name = "{name}-{source}".format(source=source, name=self.name)

    def execute(self):
        self.status = SequenceStatus.INIT
        self.status = SequenceStatus.PARSE_CRIC_FEDERATION
        CRICService.process_cric_federations(self.data["cric_federations"])
        self.status = SequenceStatus.PARSE_CRIC_SITES
        CRICService.process_cric_sites(self.data["cric_sites"])
        self.status = SequenceStatus.PARSE_REBUS_SITES
        RebusService.process_rebus_sites(self.data["rebus_sites"])
        self.status = SequenceStatus.PROCESS_SITES
        SiteService.post_process()
        self.status = SequenceStatus.ANALYSE
        SiteService.analyse(SiteService.get_all())
        self.status = SequenceStatus.END
        EventHub.announce_event(SequenceCompletedEvent(
            created_by=Sequence.__name__,
            holder=self
        ))

    def __eq__(self, other):
        if self.name is other.name and self.initial_timestamp is other.initial_timestamp:
            return True
        else:
            return False
