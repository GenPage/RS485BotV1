_sentinel = object()


class EventController:
    __event_list = {}

    @staticmethod
    def register_event_listener(event_name, function, arguments):
        if not EventController.__event_list.__contains__(function):
            EventController.__event_list[function] = {'event_name': event_name, 'arguments': arguments}

    @staticmethod
    def fire_event(event_name, *arguments):
        for function in EventController.__event_list:
            if EventController.__event_list[function]['event_name'] == event_name:
                function(*arguments)


class RegisterEvent:
    def __init__(self, event_name):
        self.event_name = event_name

    def __call__(self, func):
        EventController.register_event_listener(self.event_name, func, {})

