import socket
import queue
import threading
import subprocess
from PySide6.QtCore import QThread, Signal, QObject, Slot

from typing import List
import utils.sock as sock
from utils.sock import send_message, recv_message

def null_callback(*args):
    pass

class NetworkThread(QThread):
    finished_signal = Signal(object)
    error_signal = Signal(str)

    def __init__(self, task_queue: queue.Queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        while True:
            if not self.singel_task():
                break

    def singel_task(self):
        func, params, callback = self.task_queue.get()
        print(f"Task: {func.__name__}, {params}\n With Callback: {[callback[0].__name__, callback[1].__name__]}")
        if func is None:
            return 0
        if not callback:
            callback = [null_callback]
        call_finish = callback[0]
        call_error = callback[1] if len(callback) > 1 else call_finish
        self.finished_signal.connect(call_finish)
        self.error_signal.connect(call_error)

        try:
            response = func(*params)
            self.finished_signal.emit(response)
        except Exception as e:
            
            self.error_signal.emit(str(e))
            pass
        finally:
            self.finished_signal.disconnect(call_finish)
            self.error_signal.disconnect(call_error)
            self.task_queue.task_done()
            return 1
        
class SocketThread(QThread):
    def __init__(self):
        super().__init__()
        self.conn = None

    def run(self):
        try:
            command = [
                "C:\\Users\\Ludwig\\Python Code\\pyarticle_prj\\tools\\emb\\external.bat",
                "inference", "65432"
            ]
            subprocess.Popen(
                command, start_new_session=True, # creationflags=0x00000010,
                cwd="C:\\Users\\Ludwig\\Python Code\\pyarticle_prj\\tools\\emb"
            )
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((sock.host, sock.port))
                server_socket.listen()

                print(f"主进程在 {sock.host}:{sock.port} 等待连接...")
                conn, addr = server_socket.accept()

                with conn:
                    print(f"已连接到: {addr}")
                    self.conn = conn
                    thread = threading.Thread(target=sock.keep_alive, args=(conn,), daemon=True)
                    thread.start() # thread will exit when main thread exit safely
                    self.exec_()
                    
        except Exception as e:
            print(f"Error in SocketThread: {e}")
            return
        
    def stop(self):
        self.quit()
        self.wait()

class TempThread(QThread):    
    stream_signal = Signal(str) 
    def __init__(self, conn, message):
        super().__init__()
        self.conn = conn
        self.message = message

    def run(self):
        if self.message == 'exit':
            send_message(self.conn, 'EXIT')
            self.quit()
            return
        elif self.message == 'refresh':
            send_message(self.conn, 'REFRESH')
            return
        send_message(self.conn, self.message)

        while True:
            data = recv_message(self.conn)
            self.stream_signal.emit(data)
            if data == "[END]":
                break



class TaskQueue(QObject):
    def __init__(self, num_worker = 1):
        super().__init__()
        self.task_queue = queue.Queue()
        self.threads = [NetworkThread(self.task_queue) for _ in range(num_worker)]

        for thread in self.threads:
            thread.start()

    def add_task(self, func, params, callback: List[callable] = [null_callback]):
        self.task_queue.put((func, params, callback))

    def stop_threads(self):
        for _ in self.threads:
            self.task_queue.put((None, None))