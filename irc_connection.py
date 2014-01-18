from socket import socket
from ssl import wrap_socket
from sys import stdout
from threading import Event, Thread
from builtins import print
import traceback
from irc_events import EventController

BUFFER_LENGTH = 1024


def noop():
    pass


class IrcConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = socket()
        self.ssl_socket = wrap_socket(self.socket)

        self.closing = False

        self.recv_thread = Thread(None, self.recv_method, "IRC-Recv-Thread", (), {})
        self.recv_thread.daemon = True
        self.recv_handle_thread = Thread(None, self.recv_handle, "IRC-Recv-Handle-Thread", (), {})
        self.recv_handle_thread.daemon = True
        self.recv_handle_queue = ""
        self.recv_handle_event = Event()

    def connect(self):
        self.ssl_socket.connect((self.host, self.port))
        self.recv_handle_thread.start()
        self.recv_thread.start()

        EventController.fire_event('irc_server_connect', self)
        return True

    def receive(self, message):
        try:
            is_message = False
            if message[0] == ":":
                is_message = True
                message = message[1:]

            args = []
            message_args = message.split(' ')
            for i, v in enumerate(message_args):
                if v != str():
                    if v[0] == ":":
                        args.append(' '.join(message_args[i:])[1:])
                        break
                    else:
                        args.append(message_args[i])

            if is_message:
                if len(args) > 1:
                    sender = args[0]
                    msgtype = args[1]

                    if msgtype == "001":
                        # Welcome message: {args[2]}
                        noop()
                    elif msgtype == "002":
                        # Host message: {args[2]}
                        noop()
                    elif msgtype == "003":
                        # Server creation: {args[2]}
                        noop()
                    elif msgtype == "004":
                        # Server info: {args[2]}
                        noop()
                    elif msgtype == "005":
                        # Server modes: {args[2]}
                        noop()
                    elif msgtype == "250":
                        # Server stats: {args[2]}
                        noop()
                    elif msgtype == "251":
                        # Users and servers connected: {args[3]}
                        noop()
                    elif msgtype == "252":
                        # Operator count: {args[3]} {args[4]}
                        noop()
                    elif msgtype == "253":
                        # {args[3]} unknown connection(s)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "254":
                        # Channel count: {args[3]} {args[4]}
                        noop()
                    elif msgtype == "255":
                        # This server user and server connected: {args[4]}
                        noop()
                    elif msgtype == "265":
                        # Local users with stats: {args[3]} of max {args[4]}: {args[5]}
                        noop()
                    elif msgtype == "266":
                        # Global users with stats: {args[3]} of max {args[4]}: {args[5]}
                        noop()
                    elif msgtype == "311":
                        # User {args[3]}, ident: {args[4]}@{args[5]} {args[6]}, name: {args[7]}
                        noop()
                    elif msgtype == "312":
                        # User {args[3]} usign server {args[4]}. Server description: {args[5]}
                        noop()
                    elif msgtype == "317":
                        # User {args[3]} idle for {args[4]} seconds. Signed on at {args[5]}
                        noop()
                    elif msgtype == "318":
                        # {args[3]} End of /WHOIS list.
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "319":
                        # User {args[3]} is in channels: {args[4]}
                        noop()
                    elif msgtype == "330":
                        # User {args[3]} is logged in as {args[4]}
                        # = User {args[3]} {args[5]} {args[4]}
                        noop()
                    elif msgtype == "332":
                        # Topic on channel {args[3]}: {args[4]}
                        noop()
                    elif msgtype == "333":
                        # Topic on channel {args[3]} set by {args[4]} at time {args[5]}
                        noop()
                    elif msgtype == "353":
                        # Names list: {args[2]}
                        noop()
                    elif msgtype == "366":
                        # End of Names: {args[2]}
                        noop()
                    elif msgtype == "372":
                        # MOTD content: {args[3]}
                        noop()
                    elif msgtype == "375":
                        # MOTD start: {args[3]
                        noop()
                    elif msgtype == "376":
                        # End of /MOTD.
                        # = {args[3]}
                        EventController.fire_event('irc_server_successfully_connected', self)
                        noop()
                    elif msgtype == "401":
                        # No such nick/channel
                        noop()
                    elif msgtype == "433":
                        # {args[3]} Nickname already in use
                        # = {args[3]} {args[4]}
                        print(args[3] + " " + args[4])
                        noop()
                    elif msgtype == "671":
                        # User {args[3]} is using a secure connection
                        # = User {args[3]} {args[4]}
                        noop()
                    elif msgtype == "PRIVMSG":
                        # User {sender} sends message to {args[2]}: {args[3]}
                        EventController.fire_event('irc_privmsg_received', self, sender, args[2], args[3])
                        noop()
                    elif msgtype == "NOTICE":
                        # User {sender} sent the notice {args[3]} to {args[2]}
                        if sender == self.host:
                            EventController.fire_event('irc_server_notice', self, args[2], args[3])
                        else:
                            EventController.fire_event('irc_user_notice', self, sender, args[2], args[3])
                        noop()
                    elif msgtype == "JOIN":
                        # User {sender} joined channel {args[2]}
                        EventController.fire_event('irc_user_channel_join', self, sender, args[2])
                        noop()
                    elif msgtype == "PART":
                        # User {sender} left channel {args[2]}. Part message: {args[3]}
                        EventController.fire_event('irc_user_channel_part', self, sender, args[2], args[3])
                        noop()
                    elif msgtype == "QUIT":
                        # User {sender} quit. Quit message: {args[2]}
                        EventController.fire_event('irc_user_quit', self, sender, args[2])
                        noop()
                    elif msgtype == "NICK":
                        # User {sender} changed nick to {args[2]}
                        EventController.fire_event('irc_user_nick_change', self, sender, args[2])
                        noop()
                    elif msgtype == "MODE":
                        # User {sender} changed modes on {args[2]} to {args[3]}
                        EventController.fire_event('irc_mode_change', self, sender, args[2], args[3])
                        noop()
                    else:
                        print("Unknown message:")
                        print("  " + message)

                    EventController.fire_event('irc_message_plain', self, sender, msgtype, *args)
                else:
                    print("Weird empty message:")
                    print("  " + message)
            else:
                if len(args) > 0:
                    if args[0] == "PING":
                        self.send_method("PONG :" + args[1])
                    elif args[0] == "ERROR":
                        msg = ' '.join(args[1:])
                        if args[1] == "Closing":
                            self.force_close()
                        else:
                            EventController.fire_event('irc_server_error', self, msg)
                            print("Error: " + msg)
                    else:
                        EventController.fire_event('irc_command_plain', self, args)
                else:
                    print("Weird empty command:")
                    print("  " + message)
        except IndexError as err:
            print("Cought an error:", err)
            traceback.print_tb(err.__traceback__)

    def send_method(self, msg):
        msg = msg.strip()
        self.ssl_socket.send((msg + '\r\n').encode())
        pass

    def recv_method(self):
        while not self.closing:
            data = self.ssl_socket.recv(BUFFER_LENGTH)
            if data:
                self.recv_handle_queue += data.decode(stdout.encoding, errors='replace')
                self.recv_handle_event.set()
        pass

    def recv_handle(self):
        while not self.closing:
            if self.recv_handle_event.is_set():
                if self.recv_handle_queue != str():
                    for msg in self.recv_handle_queue.splitlines():
                        self.receive(msg)
                    self.recv_handle_queue = ""

                self.recv_handle_event.clear()

            if not self.recv_handle_event.wait(30.0) and self.recv_handle_queue != str():
                raise TimeoutException("Had a query and waited for 30 seconds..")
        pass

    def close(self):
        if not self.closing:
            self.send_method("QUIT bye")
            self.force_close()
        else:
            print("Already closed")
        pass

    def force_close(self):
        if not self.closing:
            self.closing = True
            self.ssl_socket.close()
        pass


class TimeoutException(Exception):
    def __init__(self, exception_msg):
        self.exception_msg = exception_msg

    def __str__(self):
        return self.exception_msg

