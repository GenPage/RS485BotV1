import configparser
from sys import stdin
import traceback
from irc_connection import IrcConnection

from irc_events import RegisterEvent


class Irc:
    def __init__(self, ident, this_host, nick, realname):
        self.ident = ident
        self.this_host = this_host
        self.nick = nick
        self.realname = realname
        self.irc_servers = []
        #self.event_scheduler = scheduler()

    def attach(self, host, port, options):
        new_connection = IrcConnection(self, host, port, options)
        index = len(self.irc_servers)
        if new_connection.connect():
            self.irc_servers.append(new_connection)
            return index
        else:
            print("Could not connect to the irc server")
            return -1


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_login(irc_connection):
    if irc_connection.options.__contains__('nickserv_password'):
        if len(irc_connection.options['nickserv_password']) > 0:
            irc_connection.send_method("PRIVMSG NickServ :IDENTIFY " + irc_connection.options['nickserv_password'])


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_join(irc_connection):
    if irc_connection.options.__contains__('autojoin_channels'):
        if len(irc_connection.options['autojoin_channels']) > 0:
            irc_connection.send_method("JOIN " + irc_connection.options['autojoin_channels'])


@RegisterEvent(event_name='irc_server_connect')
def send_username(irc_connection):
    irc_connection.send_method("USER " + irc.ident + " " + irc.this_host + " * :" + irc.realname)
    irc_connection.send_method("NICK " + irc.nick)


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


##
# Temporary main code here
##


def main():
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

            ident = config.get('General', 'ident')
            this_host = config.get('General', 'this_host')
            nick = config.get('General', 'nick')
            realname = config.get('General', 'realname')
            plugins = (str(config.get('General', 'plugins'))).splitlines()

            global irc
            irc = Irc(ident, this_host, nick, realname)

            for p in plugins:
                if p != str():
                    p = "plugins." + p
                    try:
                        _temp_plugin = __import__(p, globals(), fromlist=["plugins"])
                        _temp_plugin.Plugin(irc)
                        continue
                    except ImportError:
                        pass
                    except AttributeError:
                        pass

                    print("Could not load " + p)

            irc.attach(servers[0][0], servers[0][1], servers[0][2])
            return irc
    except FileNotFoundError:
        pass
    except IOError:
        pass
    except KeyError as err:
        print("There was a problem in your config.cfg")
        print(err)
        traceback.print_tb(err.__traceback__)
        return None

    print("Please create a config.cfg")
    return None


irc = main()
if irc is not None:
    if len(irc.irc_servers) > 0:
        i = 0
    else:
        i = -1

    if i != -1:
        while True:
            try:
                line = stdin.readline()
            except KeyboardInterrupt:
                break

            if not line or line.strip() == "^C":
                print()
                break

            irc.irc_servers[i].send_method(line)

        irc.irc_servers[i].close()

