_sentinel = object()


class EventController:
    __event_list = []

    @staticmethod
    def register_event_listener(event_name, function, arguments):
        EventController.__event_list.append({'event_name': event_name, 'function': function, 'arguments': arguments})

    @staticmethod
    def fire_event(event_name, *arguments):
        for event_dict in EventController.__event_list:
            if event_dict['event_name'] == event_name:
                event_dict['function'](*arguments)


class RegisterEvent:
    def __init__(self, event_name):
        self.event_name = event_name

    def __call__(self, func):
        EventController.register_event_listener(self.event_name, func, {})

