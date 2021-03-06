import abc
import datetime


class IEGLEvent:
    """ Converts an implementing class into a EGL API Event. """
    def __init__(self, created_by):
        self.data = None
        self.created_by = created_by
        self.created_on = datetime.datetime.now()


class IEGLEventListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, egl_event):
        raise NotImplementedError
