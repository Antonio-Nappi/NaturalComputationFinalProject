from Server import Server
import time
import numpy as np
from CACS import CACS

if __name__ == "__main__":
    # set numpy random seed
    np.random.seed(290796)

    # start two servers (one for each track)
    server_forza = Server('forza')
    server_forza.start()
    # server_wheel = Server('wheel')
    # server_wheel.start()
    time.sleep(10)
    dirname = 'ants_evap_1.25_seed_290796\\'
    c = CACS('default_parameters_with_bounds', dir_name=dirname, n_ants=96,
             evaporation=1.25, stop_condition=100)
    c.evolve()
