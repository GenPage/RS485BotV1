from sys import stdin
from irc_mechanics import Irc
import time

if __name__ == "__main__":
    irc = Irc.load()
    if irc is not None:
        if len(irc.irc_servers) > 0:
            i = 0
        else:
            i = -1

        if i != -1:
            if stdin.isatty():
                while True:
                    try:
                        line = stdin.readline()
                    except KeyboardInterrupt:
                        break

                    if not line or line.strip() == "^C":
                        print()
                        break

                    irc.irc_servers[i].send_method(line)
            else:
                print("No stdin, just sitting around and drinking tea")
                while True:
                    time.sleep(5)

            irc.irc_servers[i].close()
    else:
        print("There was no IRC")
    print("Closing")