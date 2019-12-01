from threading import Thread
from queue import Queue

from environ import game
from game import run
from RL import agent

def main(): 
    model = agent()
    q = Queue(1)

    train_agent = Thread(target=model.train, args=(q,))
    display_game = Thread(target=run, args=(q,))

    print("[*]Thread 1: Starting agent training")
    train_agent.start()

    print("[*]Thread 2: Starting display")
    display_game.start()

    train_agent.join()
    display_game.join()

if __name__ == "__main__":
    main()