import socket
import base64
import os
import json

SERVER = ('172.16.16.101', 1037)


def send_command(command_str):
    with socket.create_connection(SERVER) as sock:
        sock.sendall((command_str + "\r\n\r\n").encode())
        response = b""
        while b"\r\n\r\n" not in response:
            response += sock.recv(65536)
        return json.loads(response.decode())

def upload_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        filename = os.path.basename(filepath)
        command = f"UPLOAD {filename}||{data}"
        print("Upload:", send_command(command))
    except Exception as e:
        print("Upload gagal:", str(e))

def delete_file(filename):
    command = f"DELETE {filename}"
    print("Delete:", send_command(command))

if __name__ == '__main__':
    # Contoh pemanggilan
    upload_file('files/donalbebek.jpg')    
    delete_file('donalbebek.jpg')    
