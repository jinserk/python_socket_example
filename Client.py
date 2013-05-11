#!/usr/bin/python
###########################################################################
#
#   Client.py
#       socket client implementation
#
#   Jinserk Baik <jinserk.baik@gmail.com>
#   
#   this source code is distributed under GPL3.
#   if you clone this, then it means you'll agree the license
#
###########################################################################


import os, sys
import time, select, errno
import os.path as op
import subprocess as sp
import socket as sk

from Server import PORT, _eintr_retry, _send_to, _recv_from
from MyBase import MyBase, _catch_errors


HOST = 'localhost'


class Client(MyBase):

    def __init__(self):
        MyBase.__init__(self, debug=False)

        try:
            self.conn = sk.create_connection((HOST, PORT))
        except:
            self._server_start()
            self.conn = sk.create_connection((HOST, PORT))


    def __del__(self):
        try:
            self.conn.shutdown(sk.SHUT_RDWR)
            self.conn.close()
        except:
            pass


    def _server_start(self):
        try:
            f = op.join(op.dirname(sys.argv[0]), 'Server.py')
            proc = sp.Popen(['python', f])
            time.sleep(2)
        except:
            self._debug('failed to run server.')
            sys.exit(1)


    def Query(self, cmd, arg=None):
        _send_to(self.conn, cmd, arg)
        ans = _recv_from(self.conn)
        if ans[0] == cmd:
            return ans
        else:
            return 'error', None




if __name__ == '__main__':

    # disconnected after single query
    cli = Client()
    ans = cli.Query('test1')
    print ans

    cli = Client()
    ans = cli.Query('test2')
    print ans

    cli = Client()
    ans = cli.Query('test3')
    print ans

    cli = Client()
    ans = cli.Query('stop')


