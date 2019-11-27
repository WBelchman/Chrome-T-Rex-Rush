import numpy as np
import tensorflow as tf
from tensorflow import keras

from environ import game as environment

class agent():

    num_actions=3

    epsilon = 0.8
    decay_epsilon = 0.995
    min_epsilon = 0.1
    gamma = 0.99
    alpha = 0.01

    def __init__(self):
        self.history = np.zeros(3)
        self.env = environment()
        self.Q = av_function(self.alpha)

    def train(self, queue, num_iters=5000):
        
        for i in range(num_iters+1):
            #print("Iteration: {}".format(i))

            if i % 25 == 0:
                print("[*]Thread 1: Updating agent queue {}".format([self, i, False]))
                if queue.full(): queue.get_nowait() #Empties queue
                queue.put([self, i, False]) #Provides the display game function with the latest agent

            state, _, _ = self.env.step(0) #Sets initial state
            #print(self.history)
            self.history = np.zeros(3)

            done = False

            while not done:
                action = self.choose_action(state)
                state2, reward, done = self.env.step(action)

                #Doesn't train for every step
                for _ in range(20): 
                    if action == 1: self.env.step(0)
                    else: self.env.step(action)

                #print(self.gamma * self.max_val(state2))
                self.Q.train(state, (action - 1.0), reward + (self.gamma * self.max_val(state2)))

                state = state2

            self.env.reset()

            if self.epsilon <= self.min_epsilon:
                self.epsilon = self.min_epsilon
            else:    
                self.epsilon *= self.decay_epsilon

        input("\nPress ENTER to continue\n")

        print("[+]Thread 1: Training finished, signaling display {}".format([self, num_iters, True]))
        if queue.full(): queue.get_nowait()
        queue.put([self, num_iters, True])


    def choose_action(self, state):

        if (self.epsilon - np.random.uniform()) > 0:
            return np.random.randint(0, self.num_actions)

        else:
            for a in range(self.num_actions):
                l = self.Q.predict(state, a)

            #self.history[np.argmax(l)] += 1
            #print("[*] stdev: {}, epsilon: {}".format(round(np.std(l), 4), round(self.epsilon, 3)))

            return np.argmax(l)
  

    def max_val(self, state):
        l = []

        for a in range(self.num_actions):
            l.append(self.Q.predict(state, a))

        return max(l)


class av_function():

    def build_nn(self):
        model = keras.Sequential()
        model.add(keras.layers.Dense(25, activation=tf.nn.tanh, kernel_initializer='random_uniform', input_dim=3))
        model.add(keras.layers.Dense(1, activation=tf.nn.relu, kernel_initializer='random_uniform'))

        optimizer = keras.optimizers.SGD(lr = self.alpha)
        model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mean_squared_error"])

        model._make_predict_function()
        self.graph = tf.get_default_graph()

        return model

    def __init__(self, alpha=0.1):
        self.alpha = alpha
        self.model = self.build_nn()

    def train(self, state, action, reward):
        with self.graph.as_default():
            self.model.fit([[state + [action]]], [reward], epochs=1, verbose=0)

    def predict(self, state, action):
        with self.graph.as_default():
            return self.model.predict([[state + [action]]])

    def model_summary(self):
        print("\nValue function approximator:")
        self.model.summary()
    