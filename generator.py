import random

def maze_array(width, height):
    """
    the format for (x, y) is maze[y][x] = maze[row][col]
    """

    maze = [[' ' for _ in range(width)] for _ in range(height)]

    # add borders

    bar_char = '%'

    for row in range(height):
        maze[row][0] = bar_char
        maze[row][width-1] = bar_char

    for col in range(width):
        maze[0][col] = bar_char
        maze[height-1][col] = bar_char
    
    return maze

def clear(maze, width, height):
    """
    empties out a maze array, while leaving the border intact
    """

    for row in range(1, height-1):
        for col in range(1, width-1):
            maze[row][col] = ' ' 
    
    return maze

def populate_maze(maze, width, height, density):
    """
    use density to add barriers to interior of maze
    """
    # add barriers
    bar_char = '%'

    for row in range(1, height-1):
        for col in range(1, width-1):
            if random.random() < density:
                maze[row][col] = bar_char
    
    # add start and goal
    start_char = 'S'
    end_char = 'G'
    S_fract = 0.5
    G_fract = 0.8

    start_x, start_y, end_x, end_y = None, None, None, None

    while start_x == end_x and start_y == end_y:
        start_x, start_y = random.randint(1, int(S_fract*width)), random.randint(1, int(S_fract*height))
        end_x, end_y = random.randint(int(G_fract*width), width-2), random.randint(int(G_fract*height), height-2)
        
    start = (start_x, start_y)
    goal = (end_x, end_y)

    maze[start_y][start_x] = 'S'
    maze[end_y][end_x] = 'G'

    return maze, start, goal

def validate_maze(maze, start, goal):
    """
    checks to see whether maze is solvable
    """

    start = start
    goal = goal
    def is_valid(x, y):
        if 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] in (' ', 'S', 'G'):
            return True
        return False
    
    # define the possible moves (up, down, left , right)
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    stack = [(start[0], start[1])]  # Initialize the stack with the start position and cost
    visited = set()  # To keep track of visited cells

    while stack:
        x, y = stack.pop()
        if (x,y) == goal:
            maze[y][x] = 'G'
            return True
            
        visited.add((x, y))

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and (new_x, new_y) not in visited:
                stack.append((new_x, new_y))
                visited.add((new_x, new_y))

    # if the stack is empty and the goal is not reached
    return False

width = int(input('Enter the width of the maze: '))
height = int(input('Enter the height of the maze: '))
density = float(input('Enter the barrier density (0.0 to 0.4 for best results): '))
max_tries = 10

maze = maze_array(width, height)
count = 0
valid = False
while valid == False:
    if count > 0: # no need to clear the initial maze
        clear(maze, width, height)
    maze, start, goal = populate_maze(maze, width, height, density)
    count += 1
    valid = validate_maze(maze, start, goal)

    if count > max_tries:
        print('I have tried 1,0000 random mazes and was not able to make a solvable maze with the specified dimensions and density. Please try adjusting the parameters.')
        break
# Save the maze to a file
with open("random_maze.txt", "w+") as file:
    for row in maze:
        file.write("".join(row) + "\n")