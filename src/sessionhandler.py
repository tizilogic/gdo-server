import os
import time


class SessionHandler(object):
    def __init__(self, timeout, salt_len):
        self._timeout = timeout
        self._salt_len = salt_len
        self._sessions = {}

    def new_session(self):
        salt = hex(int().from_bytes(os.urandom(self._salt_len), 'little'))[2:]
        self._sessions[salt] = time.time()
        w = int().from_bytes(os.urandom(8), 'little') / (2 ** 64 - 1)
        time.sleep(w)
        return salt

    def cleanup(self):
        check_time = time.time()
        drop_list = []
        for s in self._sessions:
            if check_time - self._sessions[s] > self._timeout:
                drop_list.append(s)
        for s in drop_list:
            self._sessions.pop(s)

    def invalidate(self, salt):
        if salt in self._sessions:
            self._sessions.pop(salt)

    def valid(self, salt):
        self.cleanup()
        return salt in self._sessions

    def _active(self):
        self.cleanup()
        return str(self._sessions).encode()