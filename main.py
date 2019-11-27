# from multiprocessing import Process, Queue

from threading import Thread
from queue import Queue

from environ import game
from game import run
from RL import agent


#For some reason the display game slows down over time... MP might be necessary

def main():
    q = Queue(1)

    model = agent()

    train_agent = Thread(target=model.train, args=(q,))
    display_game = Thread(target=run, args=(q,))

    # train_agent = Process(target=model.train, args=(q,))
    # display_game = Process(target=run, args=(q,))

    print("[*]Thread 1: Starting agent training")
    train_agent.start()

    print("[*]Thread 2: Starting display")
    display_game.start()

    train_agent.join()
    display_game.join()

main()