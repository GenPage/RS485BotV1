import os
import sys
import codecs


class Logger:
    @staticmethod
    def init():
        sys.stdin = codecs.getreader('utf-8')(sys.stdin)
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        pass

    @staticmethod
    def print(msg='', new_line=True):
        if new_line:
            msg = (msg + os.linesep).encode('utf-8', 'replace')
            sys.stdout.buffer.write(msg)
        else:
            msg = msg.encode('utf-8', 'replace')
            sys.stdout.buffer.write(msg)
        sys.stdout.buffer.flush()