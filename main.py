from threading import Thread, Lock
from queue import Queue

from environ import game
from game import run
from RL import agent

#I think its the python GIL that causes the threads to hang rather than an error in the code
#I tried to use multiprocessing to run them separately but I couldn't share
#the model since it was not pickle-able, I want to keep the architecture but might
#have to change it

def main(): 
    model = agent()
    q = Queue(1)
    lock = Lock()

    train_agent = Thread(target=model.train, args=(q, lock))
    display_game = Thread(target=run, args=(q, lock))

    print("[*]Thread 1: Starting agent training")
    train_agent.start()

    print("[*]Thread 2: Starting display")
    display_game.start()

    train_agent.join()
    display_game.join() 

main()