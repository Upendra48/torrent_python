import bencodepy
import hashlib

def open(filepath):
    with open(filepath, 'rb') as file:
        return bencodepy.decode(file.read())

def size(torrent):
    # Assume the 'info' dictionary contains the 'length' field
    return torrent[b'info'][b'length']

def info_hash(torrent):
    # Compute the SHA-1 hash of the bencoded 'info' dictionary
    info_bytes = bencodepy.encode(torrent[b'info'])
    return hashlib.sha1(info_bytes).digest()
