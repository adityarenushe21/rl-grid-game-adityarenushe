from agent import QLearningAgent
import random, pickle

GRID = 6
ACTIONS = [(-1,0),(1,0),(0,-1),(0,1)]
GOAL = [4,4]

def move(pos, act):
    return [max(0,min(5,pos[0]+act[0])), max(0,min(5,pos[1]+act[1]))]

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def move_player(p):
    if random.random() < 0.8:
        best = None
        best_dist = 999
        for act in ACTIONS:
            nxt = move(p, act)
            d = manhattan(nxt, GOAL)
            if d < best_dist:
                best_dist = d
                best = nxt
        return best
    return move(p, random.choice(ACTIONS))

agent = QLearningAgent()

for ep in range(50000):

    player = [random.randint(0,5), random.randint(0,5)]
    agent_pos = [random.randint(0,5), random.randint(0,5)]

    while agent_pos == player:
        agent_pos = [random.randint(0,5), random.randint(0,5)]

    for step in range(60):

        state = agent.get_state(agent_pos, player)
        action = agent.choose_action(state)

        old_dist = manhattan(agent_pos, player)

        player = move_player(player)
        agent_pos = move(agent_pos, ACTIONS[action])

        new_dist = manhattan(agent_pos, player)

        if agent_pos == player:
            reward = 150
            done = True

        elif player == GOAL:
            reward = -150
            done = True

        else:
            reward = (old_dist - new_dist)*6
            reward -= 1
            done = False

        next_state = agent.get_state(agent_pos, player)
        agent.update(state, action, reward, next_state)

        if done:
            break

    if agent.epsilon > 0.05:
        agent.epsilon *= 0.998

pickle.dump(agent.q_table, open("model.pkl","wb"))
print("Training Done")