import os
from threading import Thread

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        os.system(r"pushd C:\torcs & wtorcs.exe -nofuel -nodamage -nolaptime -T .\config\raceman\quickrace.xml")


