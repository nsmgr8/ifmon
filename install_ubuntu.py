#!/usr/bin/env python

#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

import os
import glob
import shutil
import compileall
import stat
import sys

from ifmon.utils import smart_bytes

install_path = '/usr/share/ifmon'
mainfile = os.path.join(install_path, 'main.pyc')
binfile = '/usr/bin/ifmon'
cronsrc = os.path.join(install_path, 'resources/ifmon.cron')
cronfile = '/etc/cron.d/ifmon'
desktop_src = os.path.join(install_path, 'resources/ifmon.desktop')
desktop_target = os.path.expanduser('~/Desktop/ifmon.desktop')
dbpath = os.path.join(install_path, 'ifmon/db/ifmon.db')

def install_ifmon():
    pkgpath = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(install_path):
        try:
            shutil.rmtree(install_path)
        except OSError as e:
            print 'Warning: %s' % e

    shutil.copytree(pkgpath, install_path)
    gitpath = os.path.join(install_path, '.git')
    if os.path.exists(gitpath):
        shutil.rmtree(gitpath)
    compileall.compile_dir(install_path)

    def callback(arg, directory, files):
        print arg
        for f in files:
            if any([f.endswith(ext) for ext in ('.py', '.ui', '.qrc')]):
                os.remove(os.path.join(directory, f))

    os.path.walk(install_path, callback, "cleanup install folder")

    files = glob.glob(install_path + "/install*.pyc")
    for f in files:
        os.remove(os.path.join(install_path, f))

    symlinks = [(mainfile, binfile), (cronsrc, cronfile),]
    for f, s in symlinks:
        if os.path.exists(s):
            os.remove(s)
        os.symlink(f, s)

    shutil.copyfile(desktop_src, desktop_target)

    if not os.path.exists(dbpath):
        if not os.path.exists(os.path.dirname(dbpath)):
            os.makedirs(os.path.dirname(dbpath))
        with open(dbpath, 'w'):
            pass

    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | \
                 stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH | stat.S_IWOTH | \
                 stat.S_IWGRP
    os.chmod(desktop_target, permission)
    os.chmod(mainfile, permission)
    os.chmod(dbpath, permission)
    os.chmod(os.path.dirname(dbpath), permission)

def install_deps():
    import apt
    if not os.environ['USER'] == 'root':
        print 'ERROR: This program requires root access.'
        print 'Use `sudo python %s`' % sys.argv[0]
        raise SystemExit(1)

    def check_version(pkg, ver):
        return [v for v in pkg.versions if v >= ver]

    acq_progress = apt.progress.text.AcquireProgress()
    inst_progress = apt.progress.base.InstallProgress()

    cache = apt.Cache(apt.progress.text.OpProgress())
    pyqt4 = 'python-qt4'
    sqlobj = 'python-sqlobject'
    version = {pyqt4: '4.6', sqlobj: '0.7'}
    is_installed = {}
    for p in (pyqt4, sqlobj):
        is_installed[p] = cache[p].is_installed and \
                          check_version(cache[p], version[p])

    if not is_installed[pyqt4]:
        cache.update(acq_progress)
        cache.open()
        cache.commit(acq_progress, inst_progress)
        if not check_version(cache[pyqt4], version[pyqt4]):
            print 'ERROR: Could not find required pyqt4 package.'
            print 'You might try changing to main repository server.'
            raise SystemExit(1)

        cache[pyqt4].mark_install()
    elif not check_version(cache[pyqt4], version[pyqt4]):
        print "It requires ", version
        raise SystemExit(1)

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

    for f in [binfile, desktop_target, cronfile]:
        if os.path.exists(f):
            os.remove(f)

    print 'ifmon has been completely removed from your system! :('

if __name__ == '__main__':
    if '-u' in sys.argv:
        uninstall()
    else:
        install()

