from api.event_hub.event_managers import IEGLEvent


class NewDataAvailableOnlineEvent(IEGLEvent):

    def __init__(self, sequence, created_by, holder):
        super(NewDataAvailableOnlineEvent, self).__init__(sequence, created_by)
        self.data = holder


class DownloadCompletedEvent(IEGLEvent):
    def __init__(self, sequence, created_by, holder):
        super(DownloadCompletedEvent, self).__init__(sequence, created_by)
        self.data = holder


class OfflineParsingAllSitesCompletionEvent(IEGLEvent):
    def __init__(self, sequence, created_by, holder):
        super(OfflineParsingAllSitesCompletionEvent, self).__init__(sequence, created_by)
        self.data = holder


class SequenceCompletedEvent(IEGLEvent):
    def __init__(self, sequence, created_by, holder):
        super(SequenceCompletedEvent, self).__init__(self, sequence, created_by)
        self.data = holder

