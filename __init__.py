import sys
import time

from logger import Logger
from irc_mechanics import Irc


if __name__ == "__main__":
    Logger.init()

    irc = Irc.load()
    if irc is not None:
        if len(irc.irc_servers) > 0:
            i = 0
        else:
            i = -1

        if i != -1:
            if sys.stdin.isatty():
                while irc.is_alive():
                    try:
                        line = sys.stdin.readline()
                    except KeyboardInterrupt:
                        break

                    if not line or line.strip() == "^C":
                        Logger.print()
                        break

                    irc.irc_servers[i].send_method(line)
            else:
                Logger.print("No stdin, just sitting around and drinking tea")
                Logger.print()
                while irc.is_alive():
                    time.sleep(5)

            irc.irc_servers[i].close()
    else:
        Logger.print("There was no IRC")
    Logger.print("Closing")