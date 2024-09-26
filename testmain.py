import socket
import time
import threading
import struct

send_lock = threading.Lock()
recv_lock = threading.Lock()

def keep_alive(sock):
    while True:
        try:
            send_message(sock, 'PING')
            time.sleep(5)
        except Exception as e:
            print(f"Error in keep_alive: {e}")
            break

def send_message(sock, message):
    with send_lock:
        encoded_message = message.encode()
        length_prefix = struct.pack('!I', len(encoded_message))
        sock.sendall(length_prefix + encoded_message)

def recv_message(sock):
    with recv_lock:
        length_data = sock.recv(4)
        if not length_data:
            return None

        
        message_length = struct.unpack('!I', length_data)[0]
        message_data = b''
        while len(message_data) < message_length:
            packet = sock.recv(message_length - len(message_data))
            # print("packet", packet)
            if not packet:
                return None
            message_data += packet
    return message_data.decode()

def message_sender_recver(conn):
    while True:
        message = input("请输入发送给子进程的消息（或输入 'exit' 退出）：")
        if message == 'exit':
            send_message(conn, 'EXIT')
            break
        elif message == 'refresh':
            send_message(conn, 'REFRESH')
            continue
        send_message(conn, message)

        while True:
            data = recv_message(conn)
            print(data, end="", flush=True)
            if data == "[END]":
                print()
                break

def main():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"主进程在 {host}:{port} 等待连接...")
        conn, addr = server_socket.accept()

        with conn:
            print(f"已连接到: {addr}")
            thread = threading.Thread(target=keep_alive, args=(conn,), daemon=True)
            thread.start()
            message_sender_recver(conn)

            thread.join()
                
if __name__ == "__main__":
    main()