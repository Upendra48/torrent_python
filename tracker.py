from ctypes import util
import os
import socket
import struct
from urllib.parse import urlparse

import torrent_parser

def get_peers(torrent, callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    announce_url = torrent[b'announce'].decode('utf-8')
    url = urlparse(announce_url)

    # 1. Send connect request
    udp_send(sock, build_conn_req(), url)

    def handle_response(response):
        if resp_type(response) == 'connect':
            # 2. Receive and parse connect response
            conn_resp = parse_conn_resp(response)
            # 3. Send announce request
            announce_req = build_announce_req(conn_resp['connection_id'],torrent)
            udp_send(sock, announce_req, url)
        elif resp_type(response) == 'announce':
            # 4. Parse announce response
            announce_resp = parse_announce_resp(response)
            # 5. Pass peers to callback
            callback(announce_resp['peers'])

    while True:
        response, _ = sock.recvfrom(4096)
        handle_response(response)

def udp_send(sock, message, url, callback=lambda: None):
    sock.sendto(message, (url.hostname, url.port))
    callback()

def resp_type(resp):
    action = struct.unpack('>I', resp[:4])[0]
    if action == 0:
        return 'connect'
    elif action == 1:
        return 'announce'
    else:
        return 'unknown'

def build_conn_req():
     # Create a buffer with a size of 16 bytes
    buf = bytearray(16)

    # Connection ID (8 bytes)
    struct.pack_into('>I', buf, 0, 0x417)         # First part of connection ID
    struct.pack_into('>I', buf, 4, 0x27101980)    # Second part of connection ID

    # Action (4 bytes) - for connection request, action is 0
    struct.pack_into('>I', buf, 8, 0)

    # Transaction ID (4 bytes) - random bytes
    transaction_id = os.urandom(4)
    buf[12:16] = transaction_id

    return buf

def parse_conn_resp(resp):
    action = struct.unpack_from('>I', resp, 0)[0]
    transaction_id = struct.unpack_from('>I', resp, 4)[0]
    connection_id = resp[8:16]
    return {
        'action': action,
        'transaction_id': transaction_id,
        'connection_id': connection_id
    }


def build_announce_req(conn_id, torrent, port=6881):
    buf = bytearray(98)

    # Connection id
    buf[0:8] = conn_id

    # Action
    struct.pack_into('>I', buf, 8, 1)

    # Transaction id
    buf[12:16] = os.urandom(4)

    # Info hash
    buf[16:36] = torrent_parser.info_hash(torrent)

    # Peer ID
    buf[36:56] = os.urandom(20)

    # Downloaded
    buf[56:64] = b'\x00' * 8

    # Left
    struct.pack_into('>Q', buf, 64, torrent_parser.size(torrent))

    # Uploaded
    buf[72:80] = b'\x00' * 8

    # Event
    struct.pack_into('>I', buf, 80, 0)

    # IP address
    struct.pack_into('>I', buf, 84, 0)

    # Key
    buf[88:92] = os.urandom(4)

    # Num want
    struct.pack_into('>i', buf, 92, -1)

    # Port
    struct.pack_into('>H', buf, 96, port)

    return bytes(buf)


def parse_announce_resp(resp):
    def group(iterable, group_size):
        return [iterable[i:i + group_size] for i in range(0, len(iterable), group_size)]

    # Parse response data
    action = struct.unpack('>I', resp[0:4])[0]
    transaction_id = struct.unpack('>I', resp[4:8])[0]
    leechers = struct.unpack('>I', resp[8:12])[0]
    seeders = struct.unpack('>I', resp[12:16])[0]
    
    # Group peers data (each peer data is 6 bytes)
    peers_data = resp[20:]
    peer_groups = group(peers_data, 6)
    
    # Parse peer groups
    peers = []
    for peer in peer_groups:
        ip = '.'.join(str(b) for b in peer[0:4])
        port = struct.unpack('>H', peer[4:6])[0]
        peers.append({
            'ip': ip,
            'port': port
        })

    return {
        'action': action,
        'transaction_id': transaction_id,
        'leechers': leechers,
        'seeders': seeders,
        'peers': peers
    }
     
