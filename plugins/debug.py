from irc_events import RegisterEvent
from logger import Logger


class Plugin:
    def __init__(self, irc):
        self.irc = irc
        Logger.print()
        Logger.print("DEBUG mode enabled")
        Logger.print()

    @staticmethod
    @RegisterEvent(event_name='irc_message_plain')
    def print_all_messages(irc_connection, sender, msgtype, *args):
        Logger.print("<" + sender + "> (" + msgtype + "): " + ' '.join(args[2:]))

    @staticmethod
    @RegisterEvent(event_name='irc_command_plain')
    def print_all_commands(irc_connection, *args):
        Logger.print("!! (" + args[0] + "): " + ' '.join(args[1:]))