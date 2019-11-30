from threading import Thread, Lock
from queue import Queue

from environ import game
from game import run
from RL import agent


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
    display_game.join() #implement exit flag

main()