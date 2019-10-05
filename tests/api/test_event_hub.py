from django.test import TestCase
from egl_rest.api.event_hub.event_managers import IEGLEvent, IEGLEventListener
from egl_rest.api.event_hub import EventHub


# class TestEvent(IEGLEvent):
#     def __init__(self, created_by, holder):
#         super(TestEvent, self).__init__(created_by)
#         self.data = holder
#
#
# class TestListener(IEGLEventListener):
#     def __init__(self):
#         EventHub.register_listener(self, TestEvent)
#
#     def notify(self, egl_event):
#         EventHubTest.announce_status = True
#         EventHubTest.event = egl_event
#
#
# class EventHubTest(TestCase):
#
#     announce_status = False
#     event = None
#
#     def setUp(self):
#         self.test_event = TestEvent('django_tests', 'Event Testing')
#         TestListener()
#
#     def test_event_framework(self):
#         EventHub.announce_event(self.test_event)
#         self.assertEquals(self.announce_status, True)
#         self.assertEquals(self.event, self.test_event)

