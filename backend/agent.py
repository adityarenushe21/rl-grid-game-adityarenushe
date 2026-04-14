import numpy as np
import random

class QLearningAgent:
    def __init__(self):
        self.actions = [0,1,2,3]
        self.q_table = {}
        self.alpha = 0.2
        self.gamma = 0.95
        self.epsilon = 1.0

    def get_state(self, agent, player):
        return (agent[0], agent[1], player[0], player[1])

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return self.get_best_action(state)

    def get_best_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(4)
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(4)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(4)

        old = self.q_table[state][action]
        next_max = np.max(self.q_table[next_state])

        self.q_table[state][action] = old + self.alpha * (reward + self.gamma * next_max - old)