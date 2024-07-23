import bencodepy
import hashlib
import struct

def open_torrent(filepath):
    with open(filepath, 'rb') as file:
        return bencodepy.decode(file.read())

def size(torrent):
    # Assume the 'info' dictionary contains the 'length' field
    return torrent[b'info'][b'length']

def info_hash(torrent):
    # Compute the SHA-1 hash of the bencoded 'info' dictionary
    info_bytes = bencodepy.encode(torrent[b'info'])
    return hashlib.sha1(info_bytes).digest()

def size(torrent):
    info = torrent[b'info']
    
    if b'files' in info:
        # Multiple files, sum their lengths
        total_size = sum(file[b'length'] for file in info[b'files'])
    else:
        # Single file
        total_size = info[b'length']
    
    # Convert size to an 8-byte buffer
    return total_size