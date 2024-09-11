from PySide6.QtCore import QThread, Signal
import requests
import os

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"

def download_article(doi, filename, worker_handle=None):
    try:
        url = f"https://sci.bban.top/pdf/{doi}.pdf"
        response = requests.get(url, stream=True, headers={'User-Agent': user_agent})
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        worker_handle.terminate_progress.emit(f"{http_err}")
        return
    except requests.exceptions.RequestException as err:
        worker_handle.terminate_progress.emit(f"{err}")
        return

    total_size_in_bytes = int(response.headers.get('Content-Length', 0))
    block_size = 65536
    downloaded_size = 0
    former_percentage = 0

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            downloaded_size += len(data)
            percentage = int(downloaded_size / total_size_in_bytes * 100) 
            if percentage != former_percentage:
                if worker_handle is not None:
                    worker_handle.update_progress.emit(percentage)
                former_percentage = percentage
            file.write(data)

    if total_size_in_bytes != 0 and downloaded_size != total_size_in_bytes:
        worker_handle.terminate_progress.emit("file data mismatch")
        print("article download error")
        os.remove(filename)


class DownloadWorker(QThread):
    update_progress = Signal(int)
    terminate_progress = Signal(str)

    def __init__(self, doi, filename):
        QThread.__init__(self)
        self.doi = doi
        self.filename = filename
        self.flag = True

    def run(self):
        download_article(self.doi, self.filename, self)

if __name__ == "__main__":
    doi = "10.3390/pr9112029"
    filename = "downloaded_pdf.pdf"
    download_article(doi, filename)
    print(f"PDF downloaded as {filename}")