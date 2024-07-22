import bencodepy
import socket
from urllib.parse import urlparse
import threading

def listen_for_response(sock):
    while True:
        data, _ = sock.recvfrom(4096)
        print('Message is', data)

def main():
    # Read and decode the torrent file
    with open('catpicture_0002_archive.torrent', 'rb') as torrent_file:
        torrent_data = torrent_file.read()
    torrent = bencodepy.decode(torrent_data)
    
    # Parse the announce URL
    announce_url = torrent[b'announce'].decode('utf-8')
    url = urlparse(announce_url)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Create a message buffer
    my_msg = 'hello?'.encode('utf-8')
    
    # Send a message to the tracker
    sock.sendto(my_msg, (url.hostname, url.port))
    
    # Listen for a response from the tracker
    listener_thread = threading.Thread(target=listen_for_response, args=(sock,))
    listener_thread.start()

if __name__ == '__main__':
    main()
