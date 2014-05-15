from irc_events import RegisterEvent
import logging


class Plugin:
    __logger = logging.getLogger("default_irc_logger")

    def __init__(self, irc):
        self.irc = irc
        Plugin.__logger.setLevel(logging.INFO)
        print()
        print("LOGGING mode enabled")
        print()

    @staticmethod
    @RegisterEvent(event_name='irc_message_plain')
    def print_all_messages(irc_connection, sender, msgtype, *args):
        Plugin.__logger.info("<" + sender + "> (" + msgtype + "): " + ' '.join(args[2:]))

    @staticmethod
    @RegisterEvent(event_name='irc_command_plain')
    def print_all_commands(irc_connection, *args):
        Plugin.__logger.info("!! (" + args[0] + "): " + ' '.join(args[1:]))

    @staticmethod
    @RegisterEvent(event_name='irc_server_disconnect')
    def close_logger(irc_connection):
        logging.shutdown()