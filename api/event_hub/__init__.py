import datetime
import abc


class IEGLEvent:
    """ Converts an implementing class into a EGL API Event. """
    def __init__(self, sequence, created_by):
        self.data = None
        self.sequence = sequence
        self.created_by = created_by
        self.created_on = datetime.datetime.now()


class IEGLEventAnnouncer:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def announce(self):
        raise NotImplementedError


class IEGLEventListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, egl_event):
        raise NotImplementedError
