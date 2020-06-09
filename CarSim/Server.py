import os
from threading import Thread

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        os.system(r'cd C:\Program Files (x86)\torcs & wtorcs.exe -T -nofuel -nodamage .\config\raceman\quickrace.xml')