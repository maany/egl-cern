class EventHub:

    event_and_listeners = []

    @classmethod
    def announce_event(cls, event):
        for event_listener in cls.event_and_listeners:
            if event_listener['event'].__name__ is type(event).__name__ :
                listeners = event_listener['listeners']
                for listener in listeners:
                    listener.notify(event)

    @classmethod
    def register_listener(cls, listener, event):
        event_listener_pair = next((item for item in cls.event_and_listeners if item['event'].__name__ is type(event).__name__), None)
        if event_listener_pair is None:
            cls.event_and_listeners.append({
                "event": event,
                "listeners": [listener]
            })
        else:
            event_listener_pair['listeners'].append(listener)

