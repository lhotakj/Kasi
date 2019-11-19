from os import getenv
from kasi import Server

if __name__ == "__main__":
    port = getenv('KASI_PORT', 5000)
    Server.start_server(host='0.0.0.0', port=port)
