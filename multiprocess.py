from multiprocessing import Queue, Process, Pool, Event, Lock
from queue import Empty
import time
import os

def putQueue(q, finishedEvent):
    for i in range(100):
        hashValue = i % 2
        q.put(i)
    finishedEvent.set() 

def getQueue(q, finishedEvent):
    while not(q.empty() and finishedEvent.is_set()):
        try:
            print(os.getpid())
            print(q.get(block=True, timeout=0.05))
        except Empty:
            continue

if __name__ == "__main__":

    finishedEvent = Event()
    q = Queue()
    number_of_process = 2
    processes = []

    for p in range(number_of_process):
        processes.append(Process(target=getQueue, args=(q, finishedEvent)))
    
    p1 = Process(target=putQueue, args=(q, finishedEvent))
    p1.start()

    for p in processes:
        p.start()
    
    p1.join()
    
    for p in processes:
        p.join()
