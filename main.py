#!/usr/bin/env python

#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

import sys
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    if '-c' in sys.argv:
        from cli import app
    else:
        from gui import app
    app.main(sys.argv)

