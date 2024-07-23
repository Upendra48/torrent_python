import torrent_parser
import tracker

def main():
    # Open and decode the torrent file
    torrent = torrent_parser.open_torrent('catpicture_0002_archive.torrent')

    # Get peers from the tracker
    def print_peers(peers):
        print('List of peers:', peers)
    
    tracker.get_peers(torrent, print_peers)

if __name__ == '__main__':
    main()
