from socket import socket
from ssl import wrap_socket
from sys import stdout
from threading import Event, Thread
from builtins import print
from irc_events import EventController

BUFFER_LENGTH = 1024


def do_message(irc_conn, sender, msgtype, to, msg):
    EventController.fire_event("irc_message_plain", irc_conn, sender, msgtype, to, msg)

    if msgtype == "376":
        EventController.fire_event("irc_server_successfully_connected", irc_conn)
    pass


def do_command(irc_conn, args):
    if args[0] == "PING":
        irc_conn.send_method("PONG :" + args[1])
    elif args[0] == "ERROR":
        if args[1] != "Closing":
            print("Error: " + ' '.join(args[1:]))
        irc_conn.force_close()
    else:
        EventController.fire_event("irc_command_plain", irc_conn, args)
    pass


def receive(irc_conn, message):
    try:
        if message[0] == ":":
            args = message[1:].split(' ')
            sender = args[0]
            msgtype = args[1]
            if msgtype == "QUIT":
                to = ""
                msg = ' '.join(args[2:])
            else:
                to = args[2]
                msg = ' '.join(args[3:])

            do_message(irc_conn, sender, msgtype, to, msg)
        else:
            args = message.split(' ')
            for i, v in enumerate(args):
                if v[0] == ":":
                    args = args[:i + 1]
                    args[i] = (' '.join(args[i:]))[1:]
                    break

            do_command(irc_conn, args)
    except IndexError as err:
        print("Cought an error: {}", err)
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

        EventController.fire_event("irc_server_connect", self)
        return True

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
            if self.recv_handle_queue != str():
                for msg in self.recv_handle_queue.splitlines():
                    receive(self, msg)
                self.recv_handle_queue = ""

            self.recv_handle_event.clear()

            if not self.recv_handle_event.wait(30.0) and self.recv_handle_queue != str():
                raise TimeoutException("Had a query and waited for 30 seconds..")
        pass

    def close(self):
        if not self.closing:
            self.send_method("QUIT bye")
            #self.recv_thread.join(5)
            #self.recv_handle_thread.join(5)
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

