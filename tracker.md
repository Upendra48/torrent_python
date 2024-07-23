# Torrent Tracker Interaction in Python

## Overview

This project involves handling and parsing torrent files, communicating with UDP trackers, and retrieving peer information using Python.

## Dependencies

- `socket`: For creating UDP sockets.
- `struct`: For packing and unpacking binary data.
- `os`: For generating random bytes.
- `urllib.parse`: For parsing URLs.

## Functions

### `get_peers(torrent, callback)`

This function initiates the process of getting peers from a tracker. It sends a connect request and processes responses.

**Parameters:**

- `torrent`: The parsed torrent file data.
- `callback`: A function to be called with the list of peers.

### `udp_send(sock, message, url, callback=lambda: None)`

Sends a UDP message to the specified URL.

**Parameters:**

- `sock`: The socket through which the message is sent.
- `message`: The message to send.
- `url`: The URL to send the message to.
- `callback`: An optional callback function.

### `resp_type(resp)`

Determines the type of response received from the tracker.

**Parameters:**

- `resp`: The response received from the tracker.

**Returns:**

A string indicating the type of response.

### `build_conn_req()`

Builds a connection request to send to the tracker.

**Returns:**

A byte array containing the connection request.

### `parse_conn_resp(resp)`

Parses the connection response from the tracker.

**Parameters:**

- `resp`: The response received from the tracker.

**Returns:**

A dictionary containing the action, transaction ID, and connection ID.

### `build_announce_req(conn_id, torrent, port=6881)`

Builds an announce request to send to the tracker.

**Parameters:**

- `conn_id`: The connection ID from the connect response.
- `torrent`: The parsed torrent file data.
- `port`: The port number (default is 6881).

**Returns:**

A byte array containing the announce request.

### `parse_announce_resp(resp)`

Parses the announce response from the tracker.

**Parameters:**

- `resp`: The response received from the tracker.

**Returns:**

A dictionary containing action, transaction ID, leechers, seeders, and a list of peers.

## Running the Code

1. Ensure all dependencies are installed.
2. Use the following code to open a torrent file and retrieve the list of peers:

```python
import torrent_parser
from tracker import get_peers

torrent = torrent_parser.open('path/to/torrent/file')

def print_peers(peers):
    print('List of peers:', peers)

get_peers(torrent, print_peers)
