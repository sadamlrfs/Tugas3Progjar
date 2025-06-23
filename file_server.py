import socket
import logging
from file_protocol import FileProtocol

HOST = '0.0.0.0'
PORT = 1037
BUFFER_SIZE = 65536

def handle_client(conn, addr):
    logging.warning(f"[SERVER] Terhubung dengan {addr}")
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break
        data += chunk

    fp = FileProtocol()
    response = fp.proses_string(data.decode()) + "\r\n\r\n"
    conn.sendall(response.encode())
    conn.close()
    logging.warning(f"[SERVER] Koneksi ditutup: {addr}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(10)
        logging.warning(f"[SERVER] Menunggu koneksi di {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)
