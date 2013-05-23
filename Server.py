#!/usr/bin/python
###########################################################################
#
#   Server.py
#       back-end server implementation
#
#   Jinserk Baik <jinserk.baik@gmail.com>
#
#   This source code is distributed under BSD License.
#   The use of this code implies you agree the license.
#
###########################################################################


import os, sys
import time, select, errno
import datetime as dt
import os.path as op
import subprocess as sp
import multiprocessing as mp
import socket as sk
import pickle as pk

from MyBase import MyBase, _catch_errors


HOST = 'localhost'
PORT = 29417

MAX_CLIENT = 5
MAX_BUF_SIZE = 16384
TIMEOUT = 0.5


def _eintr_retry(func, *args):
    """restart a system call interrupted by EINTR.
       this function is referred from SocketServer.py in the stdlib."""
    while True:
        try:
            return func(*args)
        except (OSError, select.error) as e:
            if e.args[0] != errno.EINTR:
                raise


def _send_to(conn, cmd, arg=None):
    msg = pk.dumps([cmd, arg])
    conn.sendall(msg)


def _recv_from(conn):
    r, w, e = _eintr_retry(select.select, [conn], [], [], TIMEOUT)
    if conn in r:
        msg = conn.recv(MAX_BUF_SIZE)
    obj = pk.loads(msg)
    if len(obj) != 2:
        return 'error', None
    else:
        return obj[0], obj[1]




class Server(MyBase):

    stop = False

    def __init__(self):
        MyBase.__init__(self, debug=True)

        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.sock.settimeout(TIMEOUT)
        try:
            self.sock.bind((HOST, PORT))
            self.sock.listen(MAX_CLIENT)
            self._debug('server is started.')
        except sk.error:
            self._debug('server is already running.')
            self.Stop()


    def __del__(self):
        try:
            self.sock.close()
            self._debug('server is stopped.')
        except:
            pass


    def _check_request(self):
        try:
            r, w, e = _eintr_retry(select.select, [self.sock], [], [], TIMEOUT)
            if self.sock in r:
                client = self.sock.accept()
                self.HandleRequest(client)
                client[0].close()
        except Exception as e:
            self._debug(e)


    def Start(self):
        """Override this function to prepare main loop."""
        self.Loop()


    def Loop(self):
        """Override this function for main loop of the server."""
        while not self.stop:
            self._check_request()
            #time.sleep(TIMEOUT)


    def HandleRequest(self, client):
        """Override this function to handle the request from conn.
           Currently it just echoes the recevied messages."""
        try:
            cmd, arg = self.RecvFrom(client)
            self._debug(cmd, arg)
            self.SendTo(client, cmd, arg)
            if cmd == 'stop':
                self.Stop()
        except Exception as e:
            self._debug(e)


    def Stop(self):
        """Override this function to stop the server."""
        self.stop = True


    def SendTo(self, client, cmd, arg=None):
        _send_to(client[0], cmd, arg)


    def RecvFrom(self, client):
        return _recv_from(client[0])




if __name__ == '__main__':

    srv = Server()
    srv.Start()

