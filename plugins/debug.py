from irc_events import RegisterEvent


class Plugin:
    def __init__(self, irc):
        self.irc = irc
        print()
        print("DEBUG mode enabled")
        print()

    @staticmethod
    @RegisterEvent(event_name='irc_message_plain')
    def print_all_messages(irc_connection, sender, msgtype, *args):
        print("<" + sender + "> (" + msgtype + "): " + ' '.join(args))

    @staticmethod
    @RegisterEvent(event_name='irc_command_plain')
    def print_all_commands(irc_connection, *args):
        print("!! (" + args[0] + "): " + ' '.join(args[1:]))