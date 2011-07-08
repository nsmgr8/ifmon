#!/usr/bin/env python

#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from install_ubuntu import install_ifmon

warning = """
Thank you for choosing to install it on your Linux OS. There are couple things
you need to confirm before proceeding. This installation will only place this
package in desired folders. To run this software, you must satisfy all the
requirements. i.e., you must have

    PySide>=1.0.3 and
    SQLObeject>=0.7

installed in your system.

This installation also assumes that your OS uses cron job and a folder for job
listing exists at /etc/cron.d/. If this is not true for your system, please
try some other method of scheduling "ifmon.py" in your system.

Are you sure you want to continue with the installation? (Y/n) """

if __name__ == '__main__':
    print warning,
    if raw_input() <> 'n':
        install_ifmon()

