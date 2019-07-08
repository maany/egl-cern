from egl_rest.api.event_hub import EventHub
from egl_rest.api.event_hub.event_managers import IEGLEventListener
from egl_rest.api.event_hub.events.data_fetch_parse_events import NewDataAvailableOnlineEvent, SequenceCompletedEvent
from egl_rest.api.helpers import Singleton
from egl_rest.api.recon_chewbacca import ReconChewbacca
from egl_rest.api.sequence import Sequence, SequenceStatus
import datetime
import logging

# Get instance of logger
logger = logging.getLogger(__name__)


class SequenceService(Singleton, IEGLEventListener):

    def __init__(self):
        Singleton.__init__(self)
        self.sequence_queue = []
        EventHub.register_listener(self, NewDataAvailableOnlineEvent)
        EventHub.register_listener(self, SequenceCompletedEvent)

    def launch_new_or_queue(self, name, timestamp, data):
        new_sequence = Sequence(name, timestamp, data)
        self.sequence_queue.append(new_sequence)
        if len(self.sequence_queue) is 1:
            new_sequence.execute()

    def terminate_sequence(self, completed_sequence):
        completed_sequence_id = -1
        for index, sequence in enumerate(self.sequence_queue):
            if sequence == completed_sequence:
                completed_sequence_id = index
        if completed_sequence_id == -1:
            logger.error(
                "Cannot find Sequence {name} {timestamp} in the sequence queue. Unable to terminate Sequence".format(name=completed_sequence.name,
                                                                                        timestamp=completed_sequence.initial_timestamp))
        else:
            logger.info("Removing Sequence {name} {timestamp}".format(name=completed_sequence.name,
                                                                      timestamp=completed_sequence.initial_timestamp))
            logger.info("Sequence completed in {time}".format(time=datetime.datetime.now() - completed_sequence.initial_timestamp))

            del self.sequence_queue[completed_sequence_id]

            if len(self.sequence_queue) > 0:
                self.sequence_queue = [self.sequence_queue[-1]]
                next_sequence = self.sequence_queue[0]
                if next_sequence.status is None:
                    logger.info("Running queued sequence {sequence_name}".format(sequence_name= sequence.name))
                    next_sequence.execute()

    def notify(self, egl_event):
        if isinstance(egl_event, NewDataAvailableOnlineEvent):
            if egl_event.created_by == ReconChewbacca.__name__:
                self.launch_new_or_queue("data_processing_seq", datetime.datetime.now(), egl_event.data)

        if isinstance(egl_event, SequenceCompletedEvent):
            completed_sequence = egl_event.data
            self.terminate_sequence(completed_sequence)
