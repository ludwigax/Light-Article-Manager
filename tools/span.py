import os
import chardet
import subprocess
import tempfile
import pickle

def span_subprocess(shared_variable: dict, command: tuple):

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_name = temp_file.name
        pickle.dump(shared_variable, temp_file)
    temp_file.close()

    command = [*command, temp_file_name]
    command[0] = os.path.abspath(command[0])

    print(command)

    process = subprocess.Popen(
        command, cwd=os.path.dirname(command[0]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    stderr = process.stderr.read()
    stdout = process.stdout.read()
    process.stderr.close()
    process.stdout.close()

    process.wait()
    
    shared_variable = None
    if process.returncode != 0:
        encoding = chardet.detect(stderr)["encoding"]
        if encoding is not None:
            stdout = stdout.decode(encoding)
            stderr = stderr.decode(encoding)
            print(f"Output: {stdout.strip()}")
            print(f"Error: {stderr.strip()}")
    else:
        print("Subprocess Finished")
        with open(temp_file_name, "rb") as f:
            shared_variable = pickle.load(f)
    
    os.remove(temp_file_name)
    return shared_variable

if __name__ == '__main__':
    span_subprocess({}, "cls")