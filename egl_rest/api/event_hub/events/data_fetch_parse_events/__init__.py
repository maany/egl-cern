from egl_rest.api.event_hub.event_managers import IEGLEvent


class NewDataAvailableOnlineEvent(IEGLEvent):

    def __init__(self, created_by, holder):
        super(NewDataAvailableOnlineEvent, self).__init__(created_by)
        self.data = holder


class SequenceCreatedEvent(IEGLEvent):
    def __init__(self, created_by, holder):
        super(SequenceCreatedEvent, self).__init__(created_by)
        self.data = holder


class SequenceReprocessRequestEvent(IEGLEvent):
    def __init__(self, created_by, holder):
        super(SequenceReprocessRequestEvent, self).__init__(created_by)
        self.data = holder


class SequenceCompletedEvent(IEGLEvent):
    def __init__(self, created_by, holder):
        super(SequenceCompletedEvent, self).__init__(created_by)
        self.data = holder

