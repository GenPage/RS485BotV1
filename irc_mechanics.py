import configparser
import traceback
from irc_connection import IrcConnection
from irc_events import RegisterEvent


class Irc:
    def __init__(self):
        self.irc_servers = []
        #self.event_scheduler = scheduler()

    def __str__(self):
        return "Irc[" + self.irc_servers.__len__() + " Servers]"

    def attach(self, host, port, options):
        new_connection = IrcConnection(self, host, port, options)
        index = len(self.irc_servers)
        if new_connection.connect():
            self.irc_servers.append(new_connection)
            return index
        else:
            print("Could not connect to the irc server")
            return -1

    @staticmethod
    def load():
        try:
            config = configparser.ConfigParser()
            config.read_file(open('config.cfg'))

            servers = []
            if config.has_section("General"):
                for d in config.sections():
                    if d != "General":
                        options = {}
                        for o in config.options(d):
                            if o != 'ip' and o != 'port':
                                options[o] = config.get(d, o)
                        servers.append((config.get(d, 'ip'), config.getint(d, 'port'), options))

                plugins = (str(config.get('General', 'plugins'))).splitlines()

                irc_obj = Irc()

                for p in plugins:
                    if p != str():
                        p = "plugins." + p
                        try:
                            _temp_plugin = __import__(p, globals(), fromlist=["plugins"])
                            _temp_plugin.Plugin(irc_obj)
                            continue
                        except EnvironmentError:
                            print("Could not load " + p)
                        except IOError:
                            print("Could not load " + p)
                        except OSError:
                            print("Could not load " + p)

                irc_obj.attach(servers[0][0], servers[0][1], servers[0][2])
                return irc_obj
        except FileNotFoundError:
            pass
        except IOError as err:
            print("There was a problem with your config.cfg (IOError):")
            traceback.print_tb(err.__traceback__)
            return None
        except KeyError as err:
            print("There was a problem in your config.cfg")
            print(err)
            traceback.print_tb(err.__traceback__)
            return None

        print("Please create a config.cfg")
        return None


class Message:
    class MessageFormatError(AttributeError):
        def __init__(self, type1=None, type2=None):
            super.__init__(type1, type2)

    class Style:
        bold = '\u0002'
        underlined = '\u001F'
        italic = '\u0016'
        color = '\u0003'
        reset = '\u000F'

    class Color:
        white = 0
        black = 1
        blue = 2
        green = 3
        red = 4
        brown = 5
        purple = 6
        orange = 7
        yellow = 8
        light_green = 9
        cyan = 10
        light_cyan = 11
        light_blue = 12
        pink = 13
        grey = 14
        light_grey = 15

    def __init__(self):
        self._recipient_list = {}
        self._message = ""

    def send(self):
        if len(self._message) > 0:
            if self._recipient_list.__len__() > 0:
                for server in self._recipient_list:
                    local_recipient_list = self._recipient_list[server]
                    if len(local_recipient_list) > 0:
                        for recipient in local_recipient_list:
                            server.send_method("PRIVMSG " + recipient + " :" + self._message)
                    else:
                        raise Message.MessageFormatError("No recipients given")
            else:
                raise Message.MessageFormatError("No servers given")
        else:
            raise Message.MessageFormatError("No message given")

    def add_recipients(self, server, recipient_list):
        local_recipient_list = []
        if self._recipient_list.__contains__(server):
            local_recipient_list = self._recipient_list[server]

        for recipient in recipient_list:
            if local_recipient_list.__contains__(recipient):
                raise Message.MessageFormatError("Recipient " + recipient + " already on the list")

            local_recipient_list.append(recipient)

        self._recipient_list[server] = local_recipient_list

    def add_recipient(self, server, recipient):
        local_recipient_list = []
        if self._recipient_list.__contains__(server):
            local_recipient_list = self._recipient_list[server]

        if local_recipient_list.__contains__(recipient):
            raise Message.MessageFormatError("Recipient already on the list")

        local_recipient_list.append(recipient)

        self._recipient_list[server] = local_recipient_list

    def set_style(self, style, text_color=Color.black, background_color=Color.white):
        self._message += style
        if style == Message.Style.color:
            self._message += str(text_color) + "," + str(background_color)

    def put_message(self, msg):
        self._message += str(msg)


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_login(irc_connection):
    if irc_connection.options.__contains__('nickserv_password'):
        if len(irc_connection.options['nickserv_password']) > 0:
            message = Message()
            message.add_recipient(irc_connection, "NickServ")
            message.put_message("IDENTIFY ")
            message.put_message(irc_connection.options['nickserv_password'])
            message.send()


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_join(irc_connection):
    if irc_connection.options.__contains__('autojoin_channels'):
        if len(irc_connection.options['autojoin_channels']) > 0:
            irc_connection.send_method("JOIN " + irc_connection.options['autojoin_channels'])


@RegisterEvent(event_name='irc_server_connect')
def send_username(irc_connection):
    irc_connection.send_method("USER " + irc_connection.options['ident'] + " " + irc_connection.options['this_host']
                               + " * :" + irc_connection.options['realname'])
    irc_connection.send_method("NICK " + irc_connection.options['nick'])


@RegisterEvent(event_name='irc_server_notice')
def print_server_notice(irc_connection, receiver, message):
    print("[" + receiver + "] (NOTICE) SERVER: " + message)


@RegisterEvent(event_name='irc_user_notice')
def print_user_notice(irc_connection, user, receiver, message):
    print("[" + receiver + "] (NOTICE) " + user + ": " + message)


@RegisterEvent(event_name='irc_privmsg_received')
def print_privmsgs(irc_connection, sender, receiver, message):
    print("[" + receiver + "] " + sender + ": " + message)


@RegisterEvent(event_name='irc_user_channel_join')
def print_user_channel_join(irc_connection, user, channel):
    print("[" + channel + "] " + user + " joined.")


@RegisterEvent(event_name='irc_user_channel_part')
def print_user_channel_part(irc_connection, user, channel, message):
    print("[" + channel + "] " + user + " left: " + message)


@RegisterEvent(event_name='irc_user_quit')
def print_user_quit(irc_connection, user, message):
    print(user + " has left the server: " + message)


@RegisterEvent(event_name='irc_user_nick_change')
def print_user_nick_change(irc_connection, old, new):
    print(old + " has changed his nick to " + new)


@RegisterEvent(event_name='irc_mode_change')
def print_mode_change(irc_connection, sender, receiver, new_modes):
    print(sender + " has set the modes: " + receiver + " " + new_modes)

