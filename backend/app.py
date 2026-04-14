from flask import Flask, jsonify
from flask_cors import CORS
import random, pickle
from agent import QLearningAgent

app = Flask(__name__)
CORS(app)

GRID = 6
ACTIONS = [(-1,0),(1,0),(0,-1),(0,1)]
GOAL = [4,4]

def move(pos, act):
    return [max(0,min(5,pos[0]+act[0])), max(0,min(5,pos[1]+act[1]))]

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# LOAD MODEL
model = QLearningAgent()
model.epsilon = 0
model.q_table = pickle.load(open("model.pkl","rb"))

# GAME STATE
player = [0,0]
agent = [5,5]

player_score = 0
agent_score = 0
moves = 0

mode = "untrained"

# RESET POSITIONS
def reset_pos():
    global player, agent
    player = [0,0]
    agent = [5,5]

# RETURN STATE
def get_state():
    return {
        "player": player,
        "agent": agent,
        "goal": GOAL,
        "player_score": player_score,
        "agent_score": agent_score,
        "moves": moves
    }

# MODE SWITCH
@app.route("/mode/<m>")
def set_mode(m):
    global mode, player_score, agent_score, moves
    mode = m
    player_score = 0
    agent_score = 0
    moves = 0
    reset_pos()
    return jsonify({"mode": mode})

# RESET
@app.route("/reset")
def reset():
    global player_score, agent_score, moves
    player_score = 0
    agent_score = 0
    moves = 0
    reset_pos()
    return jsonify(get_state())

# STEP
@app.route("/step/<d>")
def step(d):
    global player, agent, player_score, agent_score, moves

    moves += 1

    moveset = {
        "up":(-1,0),"down":(1,0),
        "left":(0,-1),"right":(0,1)
    }

    # PLAYER MOVE
    player[:] = move(player, moveset[d])

    # AI MOVE
    if mode == "trained":
        s = (agent[0], agent[1], player[0], player[1])

        if s not in model.q_table:
            # 🔥 fallback greedy
            best = None
            best_dist = 999
            for act in ACTIONS:
                new = move(agent, act)
                dist = manhattan(new, player)
                if dist < best_dist:
                    best_dist = dist
                    best = new
            agent[:] = best
        else:
            act = max(range(4), key=lambda i: model.q_table[s][i])
            agent[:] = move(agent, ACTIONS[act])

    else:
        agent[:] = move(agent, random.choice(ACTIONS))

    # 🔥 GOAL DEFENSE
    if agent == GOAL and player == GOAL:
        agent_score += 10
        reset_pos()
        return jsonify(get_state())

    # SCORING
    if agent == player:
        agent_score += 10
        reset_pos()

    elif player == GOAL:
        player_score += 10
        reset_pos()

    return jsonify(get_state())

if __name__ == "__main__":
    app.run(debug=True)