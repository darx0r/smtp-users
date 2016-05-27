#!/bin/python

import socket
import sys

ARGS_APP = 0
ARGS_TARGET = 1
ARGS_USERS = 2
NUM_OF_ARGS = 3

KB = 1024
MAX_RESPONSE_BYTES = 4 * KB

def banner():

    print """\
                    _
      ___ _ __ ___ | |_ _ __      _   _ ___  ___ _ __ ___
<///// __| '_ ` _ \| __| '_ \    | | | / __|/ _ \ '__/ __|
     \__ \ | | | | | |_| |_) |   | |_| \__ \  __/ |  \__ \\
     |___/_| |_| |_|\__| .__/_____\__,_|___/\___|_|  |___////>
                       |_|  |_____|
                         BY.DARX0R
"""

def usage():
    print "{} <target> <users_file>".format(sys.argv[ARGS_APP])

def net_format(d):
    d += "\n"
    return d.encode('hex').decode('hex')

def smtp_cmd(s, cmd):

    data = net_format(cmd)
    s.send(data)
    return s.recv(2048 * 4)

def main(argc, argv):

    banner()

    if argc != NUM_OF_ARGS:
        usage()
        sys.exit(0)
    
    rport = 25
    rhost = sys.argv[ARGS_TARGET]
    users = sys.argv[ARGS_USERS]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((rhost, rport))

    # banner grab
    hello = s.recv(MAX_RESPONSE_BYTES)
    atoms = hello.split(' ')
    domain = atoms[1]

    smtp_cmd(s, "helo {}".format(domain))
    smtp_cmd(s, "mail from:<>")

    with open(argv[ARGS_USERS]) as users:

        for l in users.readlines():

            user = l.strip()
            res = smtp_cmd(s, "rcpt to:<{}>".format(user))

            if 'ok' in res.lower():
                print '[!] {} exists'.format(user)

    smtp_cmd(s, "quit")
    print "-- Done --"


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
