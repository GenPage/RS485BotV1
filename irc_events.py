import inspect

_sentinel = object()


class EventController:
    __event_list = []

    @staticmethod
    def register_event_listener(event, function, arguments):
        EventController.__event_list.append({'event': event, 'function': function, 'arguments': arguments})

    @staticmethod
    def fire_event(event, *arguments):
        for event_dict in EventController.__event_list:
            if event_dict['event'] == event:
                event_dict['function'](*arguments)


def event_irc_server_connect(func):
    event_name = inspect.stack()[0][3]
    EventController.register_event_listener(event_name, func, {})
    pass


def event_irc_server_successfully_connected(func):
    event_name = inspect.stack()[0][3]
    EventController.register_event_listener(event_name, func, {})
    pass


def event_irc_message_plain(func):
    event_name = inspect.stack()[0][3]
    EventController.register_event_listener(event_name, func, {})
    pass


def event_irc_command_plain(func):
    event_name = inspect.stack()[0][3]
    EventController.register_event_listener(event_name, func, {})
    pass

