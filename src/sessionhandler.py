import os
import time


class FileDict(object):
    """
    Simulate a dict like behavior but stores files named after the key
    containing the value as string.
    """
    def __init__(self):
        self.base_dir = os.path.join(os.path.split(__file__)[0], '.filedict')
        if not os.path.isdir(self.base_dir):
            os.makedirs(self.base_dir)

    def __getitem__(self, item):
        if item in os.listdir(self.base_dir):
            with open(os.path.join(self.base_dir, item), 'r') as f:
                return f.read()
        raise IndexError

    def __setitem__(self, key, value):
        with open(os.path.join(self.base_dir, key), 'w') as f:
            f.write(str(value))

    def __len__(self):
        return len(os.listdir(self.base_dir))

    def __contains__(self, item):
        if item in os.listdir(self.base_dir):
            return True
        return False

    def keys(self):
        return os.listdir(self.base_dir)

    def pop(self, item):
        v = self[item]
        try:
            os.unlink(os.path.join(self.base_dir, item))
        except FileNotFoundError:
            raise IndexError
        return v


class SessionHandler(object):
    def __init__(self, timeout, salt_len):
        self._timeout = timeout
        self._salt_len = salt_len
        self._sessions = FileDict()

    def new_session(self):
        salt = hex(int().from_bytes(os.urandom(self._salt_len), 'little'))[2:]
        self._sessions[salt] = time.time()
        w = int().from_bytes(os.urandom(8), 'little') / (2 ** 64 - 1)
        time.sleep(w)
        return salt

    def cleanup(self):
        check_time = time.time()
        drop_list = []
        for s in self._sessions.keys():
            if check_time - float(self._sessions[s]) > self._timeout:
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