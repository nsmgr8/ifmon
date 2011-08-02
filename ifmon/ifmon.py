#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

import os
import logging
from datetime import timedelta

from sqlobject import connectionForURI, sqlhub
from sqlobject import SQLObject, DateTimeCol, IntCol

from utils import get_uptime, get_bytes

DBPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db/ifmon.db')

class Bandwidth(SQLObject):
    booted_at = DateTimeCol()
    retrieved_at = DateTimeCol()
    received = IntCol()
    transmitted = IntCol()

    class sqlmeta:
        defaultOrder = "-booted_at"

    def __repr__(self):
        return '<%s - %s>' % (self.retrieved_at - self.booted_at,
                              self.received + self.transmitted)

    def total(self):
        return self.received + self.transmitted

    def uptime(self):
        return self.retrieved_at - self.booted_at

    def at(self, index):
        return {0: self.booted_at,
                1: self.uptime(),
                2: self.received,
                3: self.transmitted,
                4: self.total()}.get(index)

class Settings(SQLObject):
    start = DateTimeCol()

def setup_db(dbpath=DBPATH):
    connection = connectionForURI('sqlite:' + dbpath)
    sqlhub.processConnection = connection
    Bandwidth.createTable(ifNotExists=True)
    Settings.createTable(ifNotExists=True)

def save_data():
    _, received, transmitted = get_bytes()
    uptime, _ = get_uptime()
    now = DateTimeCol.now()
    boot_time = now - timedelta(seconds=uptime)
    boot_time = boot_time - timedelta(seconds=boot_time.second,
                                      microseconds=boot_time.microsecond)
    bws = Bandwidth.select(Bandwidth.q.booted_at==boot_time)
    for bw in bws:
        dr = received - bw.received
        dt = transmitted - bw.transmitted
        bw.received = received
        bw.transmitted = transmitted
        bw.retrieved_at = now
        break
    else:
        dr, dt = received, transmitted
        Bandwidth(booted_at=boot_time, retrieved_at=now, received=received,
                  transmitted=transmitted)

    return dr, dt


if __name__ == '__main__':
    try:
        setup_db()
        save_data()
    except Exception as e:
        logging.error(e)


