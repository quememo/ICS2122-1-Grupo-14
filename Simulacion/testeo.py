from multiprocessing import Process
import os
import random
import sys
from time import time


class simulation(Process):
    def __init__(self, name):
        # must call this before anything else
        Process.__init__(self)
        print(f"PARTIENDO")
        # then any other initialization
        self.name = name
        self.number = 0.0
        sys.stdout.write('[%s] created: %f\n' % (self.name, self.number))

    def run(self):
        for i in range(100000):
            print(f"ESTOY COMENZANDO {self.name}")


if __name__ == '__main__':
    start_time = time()
    sim_list = [simulation('foo'), simulation('bar')]

    for sim in sim_list:
        sim.start()
    for sim in sim_list:
        sim.join()

    print(f"\n IRL Exec: {(time() - start_time)} segundos")
