import inspect
from sys import stdin
from irc_connection import IrcConnection

from irc_events import event_irc_command_plain, \
    event_irc_message_plain, \
    event_irc_server_connect, \
    event_irc_server_successfully_connected


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


@event_irc_server_successfully_connected
def auto_login(irc_connection):
    irc_connection.send_method("PRIVMSG NickServ :IDENTIFY " + PASSWORD)


@event_irc_server_successfully_connected
def auto_join(irc_connection):
    for chn in AUTO_JOIN_CHANNELS:
        irc_connection.send_method("JOIN " + chn)


@event_irc_server_connect
def send_username(irc_connection):
    irc_connection.send_method("USER rs485 rs485.theZorro266.com * :RS485 Bot")
    irc_connection.send_method("NICK RS485")
    #irc_connection.send_method("PASS theZorro266:aQbmh6VzjSQTDdPF")


@event_irc_server_connect
def server_connect_1(irc_connection):
    print(inspect.stack()[0][3] + ": I want to be fired!")
    print(inspect.stack()[0][3] + ": Connection: " + irc_connection.host + ":" + str(irc_connection.port))


@event_irc_server_connect
def server_connect_2(irc_connection):
    print(inspect.stack()[0][3] + ": Me too")
    print(inspect.stack()[0][3] + ": Although I dont know what to do with " + irc_connection.host)


@event_irc_message_plain
def print_messages(irc_connection, sender, msgtype, to, msg):
    if not SHOW_MOTD and (msgtype == "375" or msgtype == "372" or msgtype == "376"):
        return

    if to != str() and msg != str():
        print(" <m- <" + sender + "> (" + msgtype + ") to " + to + ": " + msg)
    elif to != str():
        print(" <m- <" + sender + "> (" + msgtype + ") to " + to)
    elif msg != str():
        print(" <m- <" + sender + "> (" + msgtype + "): " + msg)
    else:
        print(" <m- <" + sender + "> (" + msgtype + ")")


@event_irc_command_plain
def print_commands(irc_connection, arguments):
    print(" <c- " + '[' + (', '.join(arguments)) + ']')


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

