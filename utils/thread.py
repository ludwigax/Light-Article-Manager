import queue
import threading
from PySide6.QtCore import QThread, Signal, QObject

from typing import List

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
        print(f"Task: {func.__name__}, {params}\n With Callback: {callback}")
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