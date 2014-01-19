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
    def __init__(self, irc_obj, host, port, options):
        self.irc_obj = irc_obj
        self.host = host
        self.port = port
        self.options = options

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

                    if msgtype == "001":  # RPL_WELCOME
                        # :Welcome to the Internet Relay Network <nick>!<user>@<host>
                        # = {args[3]}
                        noop()
                    elif msgtype == "002":  # RPL_YOURHOST
                        # :Your host is <servername>, running version <ver>
                        # = {args[3]}
                        noop()
                    elif msgtype == "003":  # RPL_CREATED
                        # :This server was created <date>
                        # = {args[3]}
                        noop()
                    elif msgtype == "004":  # RPL_MYINFO
                        # :<servername> <version> <available user modes> <available channel modes>
                        # = {args[3]}
                        noop()
                    elif msgtype == "005":  # _ NOT SPECIFIED
                        # :<server modes>
                        # {args[3]}
                        noop()
                    elif msgtype == "200":  # RPL_TRACELINK
                        # Link <version & debug level> <destination> <next server> V<protocol version>
                        #   <link uptime in seconds> <backstream sendq> <upstream sendq>
                        noop()
                    elif msgtype == "201":  # RPL_TRACECONNECTING
                        # Try. <class> <server>
                        noop()
                    elif msgtype == "202":  # RPL_TRACEHANDSHAKE
                        # H.S. <class> <server>
                        noop()
                    elif msgtype == "203":  # RPL_TRACEUNKNOWN
                        # ???? <class> [<client IP address in dot form>]
                        noop()
                    elif msgtype == "204":  # RPL_TRACEOPERATOR
                        # Oper <class> <nick>
                        noop()
                    elif msgtype == "205":  # RPL_TRACEUSER
                        # User <class> <nick>
                        noop()
                    elif msgtype == "206":  # RPL_TRACESERVER
                        # Serv <class> <int>S <int>C <server> <nick!user|*!*>@<host|server> V<protocol version>"
                        noop()
                    elif msgtype == "207":  # RPL_TRACESERVICE
                        # Service <class> <name> <type> <active type>
                        noop()
                    elif msgtype == "208":  # RPL_TRACENEWTYPE
                        # <newtype> 0 <client name>
                        noop()
                    elif msgtype == "209":  # RPL_TRACECLASS
                        # Class <class> <count>
                        noop()
                    elif msgtype == "210":  # RPL_TRACERECONNECT
                        # Unused.
                        noop()
                    elif msgtype == "211":  # RPL_STATSLINKINFO
                        # <linkname> <sendq> <sent messages> <sent Kbytes> <received messages> <received Kbytes>
                        #   <time open>
                        noop()
                    elif msgtype == "212":  # RPL_STATSCOMMANDS
                        # <command> <count> <byte count> <remote count>
                        noop()
                    elif msgtype == "219":  # RPL_ENDOFSTATS
                        # <stats letter> :End of STATS report
                        noop()
                    elif msgtype == "221":  # RPL_UMODEIS
                        # <user mode string>
                        noop()
                    elif msgtype == "234":  # RPL_SERVLIST
                        # <name> <server> <mask> <type> <hopcount> <info>
                        noop()
                    elif msgtype == "235":  # RPL_SERVLISTEND
                        # <mask> <type> :End of service listing
                        noop()
                    elif msgtype == "242":  # RPL_STATSUPTIME
                        # :Server Up %d days %d:%02d:%02d
                        noop()
                    elif msgtype == "243":  # RPL_STATSOLINE
                        # O <hostmask> * <name>
                        noop()
                    elif msgtype == "250":  # _ NOT SPECIFIED
                        # Server stats: {args[2]}
                        noop()
                    elif msgtype == "251":  # RPL_LUSERCLIENT
                        # :There are <integer> users and <integer> services on <integer> servers
                        # = {args[3]}
                        noop()
                    elif msgtype == "252":  # RPL_LUSEROP
                        # <integer> :operator(s) online
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "253":  # RPL_LUSERUNKNOWN
                        # <integer> :unknown connection(s)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "254":  # RPL_LUSERCHANNELS
                        # <integer> :channels formed
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "255":  # RPL_LUSERME
                        # :I have <integer> clients and <integer> servers
                        # = {args[3]}
                        noop()
                    elif msgtype == "256":  # RPL_ADMINME
                        # <server> :Administrative info
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "257":  # RPL_ADMINLOC1
                        # :<admin info>
                        # = {args[3]}
                        noop()
                    elif msgtype == "258":  # RPL_ADMINLOC2
                        # :<admin info>
                        # = {args[3]}
                        noop()
                    elif msgtype == "259":  # RPL_ADMINEMAIL
                        # :<admin info>
                        # = {args[3]}
                        noop()
                    elif msgtype == "261":  # RPL_TRACELOG
                        # File <logfile> <debug level>
                        noop()
                    elif msgtype == "262":  # RPL_TRACEEND
                        # <server name> <version & debug level> :End of TRACE
                        noop()
                    elif msgtype == "263":  # RPL_TRYAGAIN
                        # <command> :Please wait a while and try again.
                        # = {args[3]}
                        noop()
                    elif msgtype == "265":  # _ NOT SPECIFIED
                        # Local users with stats: {args[3]} of max {args[4]}: {args[5]}
                        noop()
                    elif msgtype == "266":  # _ NOT SPECIFIED
                        # Global users with stats: {args[3]} of max {args[4]}: {args[5]}
                        noop()
                    elif msgtype == "301":  # RPL_AWAY
                        # <nick> :<away message>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "302":  # RPL_USERHOST
                        # :[<reply>{<space><reply>}]
                        #   <reply> ::= <nick>['*'] '=' <'+'|'-'><hostname>
                        # = {args[3]}
                        noop()
                    elif msgtype == "303":  # RPL_ISON
                        # :[<nick> {<space><nick>}]
                        # = {args[3]}
                        noop()
                    elif msgtype == "305":  # RPL_UNAWAY
                        # :You are no longer marked as being away
                        # = {args[3]}
                        noop()
                    elif msgtype == "306":  # RPL_NOWAWAY
                        # :You have been marked as being away
                        # = {args[3]}
                        noop()
                    elif msgtype == "311":  # RPL_WHOISUSER
                        # <nick> <user> <host> * :<real name>
                        # = {args[3]} {args[4]} {args[5]} {args[6]} {args[7]}
                        noop()
                    elif msgtype == "312":  # RPL_WHOISSERVER
                        # <nick> <server> :<server info>
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "313":  # RPL_WHOISOPERATOR
                        # <nick> :is an IRC operator
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "314":  # RPL_WHOWASUSER
                        # <nick> <user> <host> * :<real name>
                        # = {args[3]} {args[4]} {args[5]} {args[6]} {args[7]}
                        noop()
                    elif msgtype == "315":  # RPL_ENDOFWHO
                        # <name> :End of WHO list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "317":  # RPL_WHOISIDLE
                        # <nick> <integer> :seconds idle
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "318":  # RPL_ENDOFWHOIS
                        # <nick> :End of WHOIS list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "319":  # RPL_WHOISCHANNELS
                        # <nick> :{[@|+]<channel><space>}
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "322":  # RPL_LIST
                        # <channel> <# visible> :<topic>
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "323":  # RPL_LISTEND
                        # :End of LIST
                        # = {args[3]}
                        noop()
                    elif msgtype == "324":  # RPL_CHANNELMODEIS
                        # <channel> <mode> <mode params>
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "325":  # RPL_UNIQOPIS
                        # <channel> <nickname>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "330":  # _ NOT SPECIFIED
                        # User {args[3]} is logged in as {args[4]}
                        # = User {args[3]} {args[5]} {args[4]}
                        noop()
                    elif msgtype == "331":  # RPL_NOTOPIC
                        # <channel> :No topic is set
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "332":  # RPL_TOPIC
                        # <channel> :<topic>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "333":  # _ NOT SPECIFIED
                        # Topic on channel {args[3]} set by {args[4]} at time {args[5]}
                        noop()
                    elif msgtype == "341":  # RPL_INVITING
                        # <channel> <nick>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "342":  # RPL_SUMMONING
                        # <user> :Summoning user to IRC
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "346":  # RPL_INVITELIST
                        # <channel> <invitemask>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "347":  # RPL_ENDOFINVITELIST
                        # <channel> :End of channel invite list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "348":  # RPL_EXCEPTLIST
                        # <channel> <exceptionmask>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "349":  # RPL_ENDOFEXCEPTLIST
                        # <channel> :End of channel exception list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "351":  # RPL_VERSION
                        # <version>.<debuglevel> <server> :<comments>
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "352":  # RPL_WHOREPLY
                        # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real name>
                        # = {args[3]} {args[4]} {args[5]} {args[6]} {args[7]} {args[8]} {args[9]}
                        noop()
                    elif msgtype == "353":  # RPL_NAMREPLY
                        # [=|*|@]<channel> :<nicks>
                        #   <nicks> ::= [[@|+]<nick>[ <nicks>]]
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "364":  # RPL_LINKS
                        # <mask> <server> :<hopcount> <server info>
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "365":  # RPL_ENDOFLINKS
                        # <mask> :End of LINKS list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "366":  # RPL_ENDOFNAMES
                        # <channel> :End of NAMES list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "367":  # RPL_BANLIST
                        # <channel> <banid>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "368":  # RPL_ENDOFBANLIST
                        # <channel> :End of channel ban list
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "369":  # RPL_ENDOFWHOWAS
                        # <nick> :End of WHOWAS
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "371":  # RPL_INFO
                        # :<string>
                        # = {args[3]}
                        noop()
                    elif msgtype == "372":  # RPL_MOTD
                        # :- <text>
                        # = {args[3]}
                        noop()
                    elif msgtype == "374":  # RPL_ENDOFINFO
                        # :End of INFO list
                        # = {args[3]}
                        noop()
                    elif msgtype == "375":  # RPL_MOTDSTART
                        # :- <server> Message of the day -
                        # = {args[3]}
                        noop()
                    elif msgtype == "376":  # RPL_ENDOFMOTD
                        # :End of MOTD command
                        # = {args[3]}
                        EventController.fire_event('irc_server_successfully_connected', self)
                        noop()
                    elif msgtype == "381":  # RPL_YOUREOPER
                        # :You are now an IRC operator
                        # = {args[3]}
                        noop()
                    elif msgtype == "382":  # RPL_REHASHING
                        # <config file> :Rehashing
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "383":  # RPL_YOURESERVICE
                        # You are service <servicename>
                        # = {args[3]}
                        noop()
                    elif msgtype == "391":  # RPL_TIME
                        # <server> :<string showing server's local time>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "392":  # RPL_USERSSTART
                        # :UserID   Terminal  Host
                        # = {args[3]}
                        noop()
                    elif msgtype == "393":  # RPL_USERS
                        # :<username> <ttyline> <hostname>
                        # = {args[3]}
                        noop()
                    elif msgtype == "394":  # RPL_ENDOFUSERS
                        # :End of users
                        # = {args[3]}
                        noop()
                    elif msgtype == "395":  # RPL_NOUSERS
                        # :Nobody logged in
                        # = {args[3]}
                        noop()
                    elif msgtype == "401":  # ERR_NOSUCHNICK
                        # <nickname> :No such nick/channel
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "402":  # ERR_NOSUCHSERVER
                        # <server name> :No such server
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "403":  # ERR_NOSUCHCHANNEL
                        # <channel name> :No such channel
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "404":  # ERR_CANNOTSENDTOCHAN
                        # <channel name> :Cannot send to channel
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "405":  # ERR_TOOMANYCHANNELS
                        # <channel name> :You have joined too many channels
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "406":  # ERR_WASNOSUCHNICK
                        # <nickname> :There was no such nickname
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "407":  # ERR_TOOMANYTARGETS
                        # <target> :Duplicate recipients. No message delivered
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "408":  # ERR_NOSUCHSERVICE
                        # <service name> :No such service
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "409":  # ERR_NOORIGIN
                        # :No origin specified
                        # = {args[3]}
                        noop()
                    elif msgtype == "411":  # ERR_NORECIPIENT
                        # :No recipient given (<command>)
                        # = {args[3]}
                        noop()
                    elif msgtype == "412":  # ERR_NOTEXTTOSEND
                        # :No text to send
                        # = {args[3]}
                        noop()
                    elif msgtype == "413":  # ERR_NOTOPLEVEL
                        # <mask> :No toplevel domain specified
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "414":  # ERR_WILDTOPLEVEL
                        # <mask> :Wildcard in toplevel domain
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "415":  # ERR_BADMASK
                        # <mask> :Bad Server/host mask
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "421":  # ERR_UNKNOWNCOMMAND
                        # <command> :Unknown command
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "422":  # ERR_NOMOTD
                        # :MOTD File is missing
                        # = {args[3]}
                        noop()
                    elif msgtype == "423":  # ERR_NOADMININFO
                        # <server> :No administrative info available
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "424":  # ERR_FILEERROR
                        # :File error doing <file op> on <file>
                        # = {args[3]}
                        noop()
                    elif msgtype == "431":  # ERR_NONICKNAMEGIVEN
                        # :No nickname given
                        # = {args[3]}
                        noop()
                    elif msgtype == "432":  # ERR_ERRONEUSNICKNAME
                        # <nick> :Erroneus nickname
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "433":  # ERR_NICKNAMEINUSE
                        # <nick> :Nickname is already in use
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "436":  # ERR_NICKCOLLISION
                        # <nick> :Nickname collision KILL from <user>@<host>
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "437":  # ERR_UNAVAILRESOURCE
                        # <nick/channel> :Nick/channel is temporarily unavailable
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "441":  # ERR_USERNOTINCHANNEL
                        # <nick> <channel> :They aren't on that channel
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "442":  # ERR_NOTONCHANNEL
                        # <channel> :You're not on that channel
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "443":  # ERR_USERONCHANNEL
                        # <user> <channel> :is already on channel
                        # = {args[3]} {args[4]} {args[5]}
                        noop()
                    elif msgtype == "444":  # ERR_NOLOGIN
                        # <user> :User not logged in
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "445":  # ERR_SUMMONDISABLED
                        # :SUMMON has been disabled
                        # = {args[3]}
                        noop()
                    elif msgtype == "446":  # ERR_USERSDISABLED
                        # :USERS has been disabled
                        # = {args[3]}
                        noop()
                    elif msgtype == "451":  # ERR_NOTREGISTERED
                        # :You have not registered
                        # = {args[3]}
                        noop()
                    elif msgtype == "461":  # ERR_NEEDMOREPARAMS
                        # <command> :Not enough parameters
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "462":  # ERR_ALREADYREGISTRED
                        # :Unauthorized command (already registered)
                        # = {args[3]}
                        noop()
                    elif msgtype == "463":  # ERR_NOPERMFORHOST
                        # :Your host isn't among the privileged
                        # = {args[3]}
                        noop()
                    elif msgtype == "464":  # ERR_PASSWDMISMATCH
                        # :Password incorrect
                        # = {args[3]}
                        noop()
                    elif msgtype == "465":  # ERR_YOUREBANNEDCREEP
                        # :You are banned from this server
                        # = {args[3]}
                        noop()
                    elif msgtype == "466":  # ERR_YOUWILLBEBANNED
                        # No message.
                        noop()
                    elif msgtype == "467":  # ERR_KEYSET
                        # <channel> :Channel key already set
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "471":  # ERR_CHANNELISFULL
                        # <channel> :Cannot join channel (+l)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "472":  # ERR_UNKNOWNMODE
                        # <char> :is unknown mode char to me
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "473":  # ERR_INVITEONLYCHAN
                        # <channel> :Cannot join channel (+i)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "474":  # ERR_BANNEDFROMCHAN
                        # <channel> :Cannot join channel (+b)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "475":  # ERR_BADCHANNELKEY
                        # <channel> :Cannot join channel (+k)
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "476":  # ERR_BADCHANMASK
                        # <channel> :Bad Channel Mask
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "477":  # ERR_NOCHANMODES
                        # <channel> :Channel doesn't support modes
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "478":  # ERR_BANLISTFULL
                        # <channel> <char> :Channel list is full
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "481":  # ERR_NOPRIVILEGES
                        # :Permission Denied- You're not an IRC operator
                        # = {args[3]}
                        noop()
                    elif msgtype == "482":  # ERR_CHANOPRIVSNEEDED
                        # <channel> :You're not channel operator
                        # = {args[3]} {args[4]}
                        noop()
                    elif msgtype == "483":  # ERR_CANTKILLSERVER
                        # :You cant kill a server!
                        # = {args[3]}
                        noop()
                    elif msgtype == "484":  # ERR_RESTRICTED
                        # :Your connection is restricted!
                        # = {args[3]}
                        noop()
                    elif msgtype == "485":  # ERR_UNIQOPPRIVSNEEDED
                        # :You're not the original channel operator
                        # = {args[3]}
                        noop()
                    elif msgtype == "491":  # ERR_NOOPERHOST
                        # :No O-lines for your host
                        # = {args[3]}
                        noop()
                    elif msgtype == "501":  # ERR_UMODEUNKNOWNFLAG
                        # :Unknown MODE flag
                        # = {args[3]}
                        noop()
                    elif msgtype == "502":  # ERR_USERSDONTMATCH
                        # :Cant change mode for other users
                        # = {args[3]}
                        noop()
                    elif msgtype == "671":  # _ NOT SPECIFIED
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
                        EventController.fire_event('irc_command_plain', self, *args)
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

