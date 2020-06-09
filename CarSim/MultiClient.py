import concurrent.futures
import sys
from client import initialize_car,Track,drive
import snakeoil
import threading
import pygmo
def thread_function(port,T):
    C = snakeoil.Client(p=port)
    if C.stage == 1 or C.stage == 2:
        try:
            T.load_track(C.trackname)
        except:
            print("Could not load the track: %s" % C.trackname)
            sys.exit()
        print("Track loaded!")
    initialize_car(C)
    C.S.d['stucktimer'] = 0
    C.S.d['targetSpeed'] = 0
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        drive(C, step)
        C.respond_to_server()
    if not C.stage:
        T.write_track(C.trackname)
    C.R.d['meta'] = 1
    C.respond_to_server()
    C.shutdown()


if __name__ == "__main__":
    T = Track()
    threads = list()
    for i in range(3):
         port = 3001+i
         x = threading.Thread(target=thread_function, args=(port,T))
         threads.append(x)
         x.start()
    for thread in threads:
        thread.join()