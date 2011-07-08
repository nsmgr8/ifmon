#!/usr/bin/env python

#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

import os
import apt
import subprocess
import glob
import shutil
import py_compile
import stat
import sys

from utils import smart_bytes

install_path = '/usr/share/ifmon'
main_pyc = os.path.join(install_path, 'main.pyc')
pngfile = os.path.join(install_path, 'ifmon.png')
cronfile = '/etc/cron.d/ifmon'
binfile = '/usr/bin/ifmon'
desktop_launcher = os.path.expanduser('~/Desktop/ifmon.desktop')
dbpath = os.path.join(install_path, 'db/ifmon.db')

def install_ifmon():
    for f in [install_path, os.path.dirname(dbpath)]:
        if not os.path.exists(f):
            try:
                os.makedirs(f)
            except OSError as e:
                print 'Warning: %s' % e

    pyfiles = [f for f in glob.glob('*.py') if not f.startswith('install')]
    installed_py = [os.path.join(install_path, f) for f in pyfiles]
    for src, dest in zip(pyfiles, installed_py):
        shutil.copyfile(src, dest)
        py_compile.compile(dest)
        os.remove(dest)

    shutil.copyfile('ifmon.png', pngfile)
    shutil.copyfile('ifmon.desktop', desktop_launcher)
    shutil.copyfile('ifmon.cron', cronfile)

    try:
        with file(dbpath, 'r'):
            print 'Using an exisiting database.'
    except IOError:
        with file(dbpath, 'w'):
            pass

    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | \
                 stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH | stat.S_IWOTH | \
                 stat.S_IWGRP
    os.chmod(desktop_launcher, permission)
    os.chmod(main_pyc, permission)
    os.chmod(os.path.dirname(dbpath), permission)
    os.chmod(dbpath, permission)

    if os.path.exists(binfile):
        os.remove(binfile)
    os.symlink(main_pyc, binfile)

def install_deps():
    if not os.environ['USER'] == 'root':
        print 'ERROR: This program requires root access.'
        print 'Use `sudo python %s`' % sys.argv[0]
        raise SystemExit(1)

    def check_version(pkg, ver):
        return [v for v in pkg.versions if v >= ver]

    acq_progress = apt.progress.text.AcquireProgress()
    inst_progress = apt.progress.base.InstallProgress()

    cache = apt.Cache(apt.progress.text.OpProgress())
    qtgui = 'python-pyside.qtgui'
    sqlobj = 'python-sqlobject'
    version = {qtgui: '1.0.3', sqlobj: '0.7'}
    is_installed = {}
    for p in (qtgui, sqlobj):
        is_installed[p] = cache[p].is_installed and \
                          check_version(cache[p], version[p])

    if not is_installed[qtgui]:
        print "It requires ", version
        print 'Do you want to install it from PPA? (Y/n)',
        if raw_input() == 'n':
            print 'ERROR: Could not install it. Quitting...'
            raise SystemExit(1)

        command = 'add-apt-repository ppa:pyside'.split()
        try:
            subprocess.check_call(command)
            cache.update(acq_progress)
            cache.open()
            cache.commit(acq_progress, inst_progress)
            if not check_version(cache[qtgui], version[qtgui]):
                print 'ERROR: Could not find required pyside package.'
                print 'You might try changing to main repository server.'
                raise SystemExit(1)
        except Exception as e:
            print 'ERROR: Could not add PPA repository. Quitting...'
            print e
            raise SystemExit(1)

        cache[qtgui].mark_install()

    if not is_installed[sqlobj]:
        cache[sqlobj].mark_install()

    if cache.install_count > 0:
        print "Need to download %.2f %s." \
                % smart_bytes(cache.required_download)
        print "Do you want to continue? (Y/n)",
        if raw_input() == 'n':
            raise SystemExit(1)
        cache.commit(acq_progress, inst_progress)

def install():
    install_deps()
    install_ifmon()
    print
    print 'Installation is successful!'
    print 'You can run it by the command `ifmon` in the terminal, or'
    print 'by clicking on the icon named `ifmon` installed on your desktop.'

def uninstall():
    if not os.path.exists(install_path):
        print "You haven't installed it yet!"
        return

    print 'Are you sure to uninstall ifmon from your system? (y/N)',
    if raw_input() <> 'y':
        print 'Thanks for keeping it. :)'
        return

    try:
        shutil.rmtree(install_path)
    except OSError as e:
        print 'Warning: %s' % e

    for f in [binfile, desktop_launcher, cronfile]:
        if os.path.exists(f):
            os.remove(f)

    print 'ifmon has been completely removed from your system! :('

if __name__ == '__main__':
    if '-u' in sys.argv:
        uninstall()
    else:
        install()

