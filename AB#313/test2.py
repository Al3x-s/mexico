
from threading import Thread
waiting_time = 0.05
def check():
    i = input()
    global waiting_time
    waiting_time = 0
Thread(target = check).start()

import sys,time,random

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(waiting_time)

print_slow("Type fasldfhasldfhais'dajs something here slowly")
