class CaveArea:
    def __init__(self, filename):
        self.filename = filename
        self.cave_map = []
        self.complete_cave = []
        self.rows = 0
        self.columns = 0

    def get_map(self):
        file = open(self.filename, "r")
        data = file.read().split("\n")
        for i in data:
            self.cave_map.append(i.split(","))
        self.rows = len(self.cave_map)
        self.columns = len(self.cave_map[0])
        self.cave_map = self.cave_map[::-1]
        self.cave_map = [[row[i] for row in self.cave_map] for i in range(len(self.cave_map[0]))]

    def mapped_cave(self):
        i = 0
        around = []
        self.complete_cave = [[] for i in range(self.rows)]
        while i < self.rows:
            j = 0
            while j < self.columns:
                dialogue = []
                mid = self.cave_map[i][j]
                if i == 0 and j == 0:
                    around = [self.cave_map[i+1][j], self.cave_map[i][j+1]]
                elif i == 0 and j != 0 and j < self.columns-1:
                    around = [self.cave_map[i-1][j], self.cave_map[i+1][j], self.cave_map[i][j+1]]
                elif i == 0 and j != 0 and j == self.columns-1:
                    around = [self.cave_map[i+1][j], self.cave_map[i][j-1]]                
                elif i != 0 and j == 0 and i < self.rows-1:
                    around = [self.cave_map[i][j+1], self.cave_map[i][j-1], self.cave_map[i+1][j]]
                elif i != 0 and j != 0 and i < self.rows-1 and j < self.columns-1:
                    around = [self.cave_map[i-1][j], self.cave_map[i+1][j], self.cave_map[i][j+1], self.cave_map[i][j-1]]
                elif i != 0 and j != 0 and i < self.rows-1:
                    around = [self.cave_map[i-1][j], self.cave_map[i+1][j], self.cave_map[i][j-1]]
                
                if "W" in around:
                    dialogue.append("There is a STENCH. Wumpus can be around.")
                if "P" in around:
                    dialogue.append("There is a BREEZE in here. There can be a pit around.")
                self.complete_cave[i].append((mid, (i+1, j+1), dialogue))
                j += 1
            i += 1
        return None
    
    def get_cave(self):
        return self.complete_cave

    def killed_wumpus(self):
        self.cave_map = [list(map(lambda x: x if x != 'W' else 'X', i)) for i in self.cave_map]
        self.mapped_cave()


class Player:
    def __init__(self):
        self.directions = ["EAST", "NORTH", "WEST", "SOUTH"]
        self.arrows = 1
        self.win = False
        self.dead = False
        self.direction = 0
        self.position = (1, 1)

    def turn_right(self):
        if self.direction == 3:
            self.direction = 0
        else:
            self.direction += 1
        
    def get_position(self):
        return self.position
    
    def set_position(self, x, y):
        self.position = (x, y)

    def turn_left(self):
        if self.direction == 0:
            self.direction = 3
        else:
            self.direction -= 1
    
    def get_direction(self):
        return self.directions[self.direction]

    def fire(self):
        self.arrows = 0

    def won(self):
        self.win = True
    
    def get_win(self):
        return self.win
    
    def died(self):
        self.dead = True

    def get_dead(self):
        return self.dead
    
    def get_win(self):
        return self.win
    
    def get_arrow(self):
        return self.arrows

def get_dialogue(cave_map, x, y):
    dialogue = []
    for i in cave_map:
        for j in i:
            if j[1] == (x, y):
                return [j[2], j[0]]
    return [dialogue, 0]

def get_wumpus(cave_map, x, y, dir):
    pos = []
    if dir == "EAST":
        for i in cave_map:
            for j in i:
                if j[1][1] == y and j[1][0] > x:
                    pos.append(j[0])

    elif dir == "SOUTH":
        for i in cave_map:
            for j in i:
                if j[1][1] < y and j[1][0] == x:
                    pos.append(j[0])
    elif dir == "WEST":
        for i in cave_map:
            for j in i:
                if j[1][1] == y and j[1][0] < x:
                    pos.append(j[0])
    elif dir == "NORTH":
        for i in cave_map:
            for j in i:
                if j[1][1] > y and j[1][0] == x:
                    pos.append(j[0])
    return pos 

def main():
    cave = CaveArea("wumpus.txt")
    cave.get_map()
    cave.mapped_cave()
    player = Player()
    while not player.get_dead() and player.get_win() == False:
        print("You are in room [%d, %d]. Facing %s. " %(player.get_position()[0], player.get_position()[1], player.get_direction()))
        dialogues = get_dialogue(cave.get_cave(), player.get_position()[0], player.get_position()[1])
        if dialogues != []:
            for i in dialogues[0]:
                print(i)
        choice = input("What would you like to do? Please enter command [R,L,F,S]:")
        if choice == "R":
            player.turn_right()
        
        elif choice == "L":
            player.turn_left()
        
        elif choice == "F":
            x, y = player.get_position()
            cave_x = cave.columns
            cave_y = cave.rows
            if player.get_direction() == "EAST":
                if x < cave_x:
                    x += 1
                    player.set_position(x, y)
                    dialogues = get_dialogue(cave.get_cave(), player.get_position()[0], player.get_position()[1])
                    if dialogues[1] == "P":
                        print("You have fallen into a pit. You are dead")
                        player.died()
                    elif dialogues[1] == "W":
                        print("You were eaten by the Wumpus. You are dead.")
                        player.died()
                    elif dialogues[1] == "G":
                        print("You have found Gold. You win")
                        player.won()
                elif x == cave_x:
                    print("BUMP!!! You hit a wall!")
            elif player.get_direction() == "WEST":
                if x > 1:
                    x -= 1
                    player.set_position(x, y)
                    dialogues = get_dialogue(cave.get_cave(), player.get_position()[0], player.get_position()[1])
                    if dialogues[1] == "P":
                        print("You have fallen into a pit. You are dead")
                        player.died()
                    elif dialogues[1] == "W":
                        print("You were eaten by the Wumpus. You are dead.")
                        player.died()
                    elif dialogues[1] == "G":
                        print("You have found Gold. You win")
                        player.won()
                elif x == 1:
                    print("BUMP!!! You hit a wall!")
            elif player.get_direction() == "NORTH":
                if y < cave_y:
                    y += 1
                    player.set_position(x, y)
                    dialogues = get_dialogue(cave.get_cave(), player.get_position()[0], player.get_position()[1])
                    if dialogues[1] == "P":
                        print("You have fallen into a pit. You are dead")
                        player.died()
                    elif dialogues[1] == "W":
                        print("You were eaten by the Wumpus. You are dead.")
                        player.died()
                    elif dialogues[1] == "G":
                        print("You have found Gold. You win")
                        player.won()
                elif y == cave_y:
                    print("BUMP!!! You hit a wall!")
            elif player.get_direction() == "SOUTH":
                if y > 1:
                    y -= 1
                    player.set_position(x, y)
                    dialogues = get_dialogue(cave.get_cave(), player.get_position()[0], player.get_position()[1])
                    if dialogues[1] == "P":
                        print("You have fallen into a pit. You are dead")
                        player.died()
                    elif dialogues[1] == "W":
                        print("You were eaten by the Wumpus. You are dead.")
                        player.died()
                    elif dialogues[1] == "G":
                        print("You have found Gold. You win")
                        player.won()
                elif y == 1:
                    print("BUMP!!! You hit a wall!")
        elif choice == "S":
            x, y = player.get_position()
            cave_x = cave.columns
            cave_y = cave.rows
            if player.get_arrow() == 1:
                cells = get_wumpus(cave.complete_cave, x, y, player.get_direction())
                if "W" in cells:
                    print("SCREAM")
                    print("You have killed the Wumpus.")
                    cave.killed_wumpus()
                    player.fire()
                else:
                    print("You have wasted your arrow.")
                    player.fire()
            else:
                print("You don't have an arrow to fire.")


if __name__ == "__main__":
    main()
