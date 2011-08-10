Bandwidth Monitor (ifmon)
=========================

:Author: M Nasimul Haque
:Web: http://www.nasim.me.uk

A simple desktop viewer for your Linux network bandwidth usage.

Screenshot
==========

.. image:: https://lh3.googleusercontent.com/-bmYNXSV0xJU/Tj0nmYTjL8I/AAAAAAAAAmc/E5i14-ty0Yk/s1024/Screenshot.png

Requirements
============

This is built on PySide - a python binding for Qt4 by Nokia. A Qt4 runtime
along with a python installation is required. It also requires SQLObject, a
python based ORM.

Installation
============

Download the source code from github_ and unzip it to a folder. The rest of the
document assumes that it has been downloaded to **~/Downloads** folder and
extracted to **ifmon** folder.

Ubuntu (>= Lucid)
-----------------

The source distribution includes a install script for Ubuntu (including Lucid
and greater). To install it just open up a terminal and run the following
commands.::

    $ cd ~/Downloads/ifmon/
    $ ./install_ubuntu.sh

This will install all the dependencies and ifmon itself. After a successful
installation, you can run ifmon either from the command line through
**ifmon** command or double click the shortcut installed on your desktop.

There is a text-based UI available also for terminal-environment. You can run
it via the command ``ifmon -c``.

Other Linux
-----------

For other linux distributions you need to install the following from your
package manager.

    1. pyside >= 1.0.3
    2. python SQLObject >= 0.7
    3. python urwid >= 0.9 

After satisfying the requirements you can either double click the **main.py**
file or run it from the commandline via::

    $ cd ~/Downloads/ifmon
    $ sudo python install_other.py

Note that, this installation also assumes that your OS uses cron job and a
folder for job listing exists at **/etc/cron.d/**. If this is not true for your
system, please try some other method of scheduling **ifmon.py** in your system.

Bug Report/Feature Request
--------------------------

Please use this `github issue page <https://github.com/nsmgr8/ifmon/issues>`_
for the bug reports and feature requests. Thanks. 

License
=======

The source code is licensed under MIT license. Please hack it to suit yourself
or even better contribute your code or suggestions to it.

The MIT License (MIT)
---------------------

Copyright (c) 2011 M. Nasimul Haque

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

.. _github: https://github.com/nsmgr8/ifmon

