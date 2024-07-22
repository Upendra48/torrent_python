import os

class Util:
    _id = None

    @staticmethod
    def gen_id():
        if Util._id is None:
            Util._id = bytearray(20)
            random_bytes = os.urandom(12)
            prefix = b'-PC0001-'  # Adjust prefix as necessary
            Util._id[:len(prefix)] = prefix
            Util._id[len(prefix):] = random_bytes
        return bytes(Util._id)