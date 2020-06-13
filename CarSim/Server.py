import os
from threading import Thread

class Server(Thread):
    def __init__(self,track):
        self.track = track
        Thread.__init__(self)

    def run(self):
        os.system(r"pushd C:\torcs_{} & wtorcs.exe -nofuel -nodamage -nolaptime -T -t 1000000000 .\config\raceman\quickrace.xml >NUL".format(self.track))


