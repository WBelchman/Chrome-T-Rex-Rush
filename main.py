from multiprocessing import Process

from environ import game
from game import run
from RL import agent


def main():
    model = agent()

    iters = 0 #The amount of training iterations

    display_game = Process(target=run, args=(iters, model))
    train_agent = Process(target=model.train)

main()