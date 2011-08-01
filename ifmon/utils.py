#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

def get_uptime():
    with file('/proc/uptime', 'r') as f:
        uptime = f.read()
    return [float(u) for u in uptime.split()]

def get_bytes():
    with file('/proc/net/dev', 'r') as f:
        devs = f.read()

    received, transmitted = 0, 0
    devices = 'eth', 'wlan', 'ppp'
    for line in devs.splitlines()[2:]:
        cols = line.split(':')
        if any([cols[0].strip().startswith(dev) for dev in devices]):
            cols = cols[1].split()
            received += int(cols[0])
            transmitted += int(cols[8])

    total = received + transmitted
    return total, received, transmitted

def smart_bytes(bytes_):
    if bytes_ < 1500:
        return bytes_, 'B'
    if bytes_ < 1500000:
        return bytes_ / 1024.0, 'KB'
    if bytes_ < 1500000000:
        return bytes_ / (1024.0 * 1024.), 'MB'
    return bytes_ / (1024.0 * 1024.0 * 1024.0), 'GB'
