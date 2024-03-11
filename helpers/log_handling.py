import streamlit as st
from queue import Queue, Empty
from threading import Thread, current_thread
import sys
import subprocess
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
class Printer:
    def __init__(self):
        self.queues = {}

    def write(self, value):
        '''handle stdout'''
        queue = self.queues.get(current_thread().name)
        if queue:
            queue.put(value)
        else:
            sys.__stdout__.write(value)

    def register(self, thread):
        '''register a Thread'''
        queue = Queue()
        self.queues[thread.name] = queue
        return queue

    def flush(self):
        '''seems to be needed '''
        pass

    def clean(self, thread):
        '''delete a Thread'''
        del self.queues[thread.name]


printer = Printer()
sys.stdout = printer

class Streamer:
    def __init__(self, target, args):
        self.thread = Thread(target=target, args=args)
        self.queue = printer.register(self.thread)

    def start(self):
        self.thread.start()
        while self.thread.is_alive():
            try:
                item = self.queue.get_nowait()
                yield f'{item.strip()}'
            except Empty:
                pass
        yield 'End'
        printer.clean(self.thread)

def job(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
    for stdout_line in iter(popen.stdout.readline, ""):
        #sys.__stdout__.write(stdout_line)
        result = ansi_escape.sub('', stdout_line)
        result = result.strip()
        if result:
            print(result)
    return_code = popen.wait()
    if return_code:
        print("=========================")
        print(subprocess.CalledProcessError(return_code, cmd))
        print("=========================")
    popen.stdout.close()

def execute(cmd, placeholder,):
    output_func = getattr(placeholder, "text")
    streamer = Streamer(job, ([cmd]))
    for line in streamer.start():
        if line !="":
            output_func(line)
    
if __name__ == "__main__":
    streamer = Streamer(job, (['find', '/home/jschaef/Downloads']))
    for line in streamer.start():
       st.code(line)
    placeholder = st.columns(1)[0]
    execute(['find', '/home/jschaef/Downloads'], placeholder, 'code')
