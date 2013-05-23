python_socket_example
=====================

Server/client example using socket with polling in Python

this server / client example using socket connection is a result of my Python study.
The server just polls any request from a client, echoes back, then disconnect the connection.
I borrowed the EINTR reset concept from the SocketServer in Python stdlib.
If you want to make your own server using this source, just inherit the client and the server respectively,
then override the Start(), Stop(), Loop(), and HandleRequest() functions in the server.

This source code is distributed under BSD License.
The use of this code implies you agree the license.

Copyright (c) 2013, Jinserk Baik All rights reserved.
