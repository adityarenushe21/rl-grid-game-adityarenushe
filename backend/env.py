import random
import time

GRID_SIZE = 6

# Directions: up, down, left, right
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = [0, 0]
        self.agent = [5, 5]
        self.goal = [2, 2]
        self.done = False

    def move(self, position):
        move = random.choice(actions)
        new_pos = [position[0] + move[0], position[1] + move[1]]

        # Keep inside grid
        new_pos[0] = max(0, min(GRID_SIZE - 1, new_pos[0]))
        new_pos[1] = max(0, min(GRID_SIZE - 1, new_pos[1]))

        return new_pos

    def step(self):
        if self.done:
            return

        # Move player
        self.player = self.move(self.player)

        # Move agent
        self.agent = self.move(self.agent)

        # Check conditions
        if self.agent == self.player:
            print("🤖 Agent caught the player!")
            self.done = True

        elif self.player == self.goal:
            print("🏁 Player reached the goal!")
            self.done = True

    def render(self):
        grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        px, py = self.player
        ax, ay = self.agent
        gx, gy = self.goal

        grid[px][py] = "P"
        grid[ax][ay] = "A"
        grid[gx][gy] = "G"

        print("\n" * 2)
        for row in grid:
            print(" ".join(row))

# Run game
game = Game()

for step in range(30):
    game.render()
    game.step()
    time.sleep(0.5)

    if game.done:
        break