"""
Server that accepts encrypted messages to set a GPIO pin to high upon valid
request from a client.
"""

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.1'
__copyright__ = """Copyright (c) 2019 Tiziano Bettio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import hashlib
import threading
import sys
import os

path = os.path.split(__file__)[0]
if path not in sys.path:
    sys.path.insert(0, path)
if os.getcwd() != path:
    os.chdir(path)

import opener
from settings import PASSPHRASE
from settings import TIMEOUT
from settings import SALT_LEN

from sessionhandler import SessionHandler

session_handler = SessionHandler(TIMEOUT, SALT_LEN)


def application(environ, start_response):
    session_handler.cleanup()
    if environ['PATH_INFO'] == '/salt':
        response_body = session_handler.new_session().encode()
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]
    elif environ['PATH_INFO'] == '/':
        response_body = open('snippets/form.html', 'r').read()
        response_body = response_body.replace('@@salt@@',
                                              session_handler.new_session())
        response_body = response_body.encode()
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ]
    elif environ['PATH_INFO'] == '/open':
        q_split = environ['QUERY_STRING'].split('=')
        response_body = open('snippets/invalid.html', 'r').read().encode()
        if len(q_split) == 2:
            salt, hashstring = q_split
            if session_handler.valid(salt):
                session_handler.invalidate(salt)
                hm = hashlib.sha3_512()
                raw = PASSPHRASE + salt
                hm.update(raw.encode())
                chk_hashstring = hm.hexdigest()
                if hashstring == chk_hashstring:
                    t = threading.Thread(target=opener.open_door)
                    t.start()
                    response_body = open('snippets/success.html', 'r').read()
                    response_body = response_body.encode()

        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ]
    else:
        # instead of 404, just send random amount of random hex data...
        num_bytes = int().from_bytes(os.urandom(2), 'little') // 2 + 1
        response_body = hex(int().from_bytes(os.urandom(num_bytes), 'little'))
        response_body = response_body[2:].encode()
        # response_body =  session_handler._active() !!!DEBUGGING ONLY!!!
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]

    start_response(status, response_headers)
    return [response_body]

