import socket
import sys
import struct
import threading

from llama import *

send_lock = threading.Lock()
recv_lock = threading.Lock()

def send_message(sock, message):
    with send_lock:
        encoded_message = message.encode()
        print(len(encoded_message))
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
            print("packet", packet)
            if not packet:
                return None
            message_data += packet
    return message_data.decode()

def main(port):
    host = '127.0.0.1'
    meta = prepare_model()
    conversation = Message()
    import copy
    
    with open("messages.json", "r", encoding="utf-8") as f:
        conversation._dict = json.load(f)
        conversation.print()

    first_conversation = copy.deepcopy(conversation)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
        except Exception as e:
            print(f"连接失败: {e}")
            sys.exit(1)

        send_obscene = lambda x: send_message(client_socket, x)

        while True:
            data = recv_message(client_socket)
            if data is None:
                break

            if data == 'EXIT':
                print("Remote Exit")
                with open("messages.json", "w", encoding="utf-8") as f:
                    json.dump(conversation.dict(), f, indent=4, ensure_ascii=False)
                break
            elif data == 'PING':
                print("Remote Ping")
                continue
            elif data == 'REFRESH':
                print("Remote refresh")
                conversation = copy.deepcopy(first_conversation)
                continue

            print("user:", data)
            conversation.add_role("user", data)

            model, tokenizer, streamer = meta.values()
            inputs = tokenizer.apply_chat_template(
                conversation.dict(),
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
                **TOKENIZER_KWARGS,
            )

            generative_kwargs = {
                **inputs, **GENERATION_KWARGS, "streamer": streamer
            }
            thread = stream_start(model, generative_kwargs)
            generate_text = stream_generate_call(streamer, send_obscene)
            conversation.add_role("assistant", generate_text)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python child.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    main(port)

    


    