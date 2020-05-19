
import time

import multiprocessing

from tests.test_constants import DEFAULT_JOIN_DURATION

def start_proccesses(run_function, service_ids_list):
    proccesses = []
    for service_id in service_ids_list:   
        proccess = multiprocessing.Process(target=run_function, args=[ service_id ])
        proccess.start()  
        proccesses.append(proccess)
    return proccesses

def stop_proccesses(proccesses, processing_wait_duration):
    time.sleep(processing_wait_duration)
    for proccess in proccesses:
        proccess.join(DEFAULT_JOIN_DURATION)
        proccess.kill()
        