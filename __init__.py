from sys import stdin
from irc_mechanics import Irc

if __name__ == "__main__":
    irc = Irc.load()
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
