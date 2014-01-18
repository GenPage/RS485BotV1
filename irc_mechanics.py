from sys import stdin
from irc_connection import IrcConnection

from irc_events import RegisterEvent


PASSWORD = "2o9oRsVz3dqsdoMdzYFg"
AUTO_JOIN_CHANNELS = ["#RS485"]

SHOW_MOTD = False


class Irc:
    def __init__(self):
        self.irc_servers = []
        #self.event_scheduler = scheduler()

    def attach(self, host, port):
        new_connection = IrcConnection(host, port)
        index = len(self.irc_servers)
        if new_connection.connect():
            self.irc_servers.append(new_connection)
            return index
        else:
            print("Could not connect to the irc server")
            return -1


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_login(irc_connection):
    irc_connection.send_method("PRIVMSG NickServ :IDENTIFY " + PASSWORD)


@RegisterEvent(event_name='irc_server_successfully_connected')
def auto_join(irc_connection):
    for chn in AUTO_JOIN_CHANNELS:
        irc_connection.send_method("JOIN " + chn)


@RegisterEvent(event_name='irc_server_connect')
def send_username(irc_connection):
    irc_connection.send_method("USER rs485 rs485.theZorro266.com * :RS485 Bot")
    irc_connection.send_method("NICK RS485")


@RegisterEvent(event_name='irc_server_notice')
def print_server_notice(irc_connection, receiver, message):
    print_user_notice(irc_connection, "SERVER", receiver, message)


@RegisterEvent(event_name='irc_user_notice')
def print_user_notice(irc_connection, user, receiver, message):
    print("[NOTICE] to " + receiver + " " + user + ": " + message)


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

irc_obj = Irc()
i = irc_obj.attach("availo.esper.net", 6697)

if i != -1:
    while True:
        try:
            line = stdin.readline()
        except KeyboardInterrupt:
            break

        if not line or line.strip() == "^C":
            print()
            break

        irc_obj.irc_servers[i].send_method(line)

    irc_obj.irc_servers[i].close()

