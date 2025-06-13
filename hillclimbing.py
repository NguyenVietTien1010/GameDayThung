import pygame
import heapq
from random import randint

# Initialize pygame
pygame.init()

# Tile size
TILE_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Maps with predefined boxes (B), goals (G), and player (P)
MAPS = [
    [  # Easy level
        "###################################",
        "#   G       ####       G          #",
        "#   ####   G      B     B        G#",
        "#   #   B         #####   B     B #",
        "# B #   G    B   G     G    G     #",
        "#   #        ####    B    ####    #",
        "#   #   G    B     ######     G   #",
        "#   ####   ####     B     ####    #",
        "#   B   B    G  B  ####    G      #",
        "#   G   ######     G        B     #",
        "#  G      B       ####      G     #",
        "#     B       ####    B       ####",
        "#      #####           G      B  #",
        "#     P         G    ####         #",
        "#   ####   B   ####               #",
        "#        G   ####         ####    #",
        "#      ####     B   ####          #",
        "#                        G        #",
        "#                  ####           #",
        "###################################"
    ],
    [  # Medium level (20x35)
        "###################################",
        "#     B   G      ####   B   G     #",
        "#     #######        ####         #",
        "#     G   B     ####   B    G     #",
        "#     #######    G    ####        #",
        "#     G   B     ####   B   B      #",
        "#     B     ######   G   B   G    #",
        "#        G    B   #######         #",
        "#   #  ####    B       G      G   #",
        "#     G      #####     B   B      #",
        "#   ####   B     G      ####      #",
        "#   B          ####   B      G    #",
        "#   G   ####   G      #######     #",
        "#     G        ###        B       #",
        "#                     ####        #",
        "#   B      G   ####      B    G   #",
        "#   G     ###          ####   B   #",
        "#     G    B   ####   B   G       #",
        "#     B         #######   G   P   #",
        "###################################"
    ]
,
    [  # Hard level (randomized 21 boxes and 21 goals)
        "###################################",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "#                                 #",
        "###################################"
    ]
]
# Function to add random walls, boxes, goals, and player to the hard level
def populate_random_hard_level_with_walls(game_map, num_boxes, num_walls):
    empty_spaces = [(x, y) for y, row in enumerate(game_map) for x, tile in enumerate(row) if tile == ' ']

    if len(empty_spaces) < 2 * num_boxes + 1 + num_walls:  # +1 for the player
        raise ValueError("Not enough empty spaces to place walls, boxes, goals, and player.")

    # Place walls
    walls = []
    for _ in range(num_walls):
        wall_pos = empty_spaces.pop(randint(0, len(empty_spaces) - 1))
        walls.append(wall_pos)

    # Place boxes and goals
    boxes = []
    goals = []
    for _ in range(num_boxes):
        box_pos = empty_spaces.pop(randint(0, len(empty_spaces) - 1))
        goal_pos = empty_spaces.pop(randint(0, len(empty_spaces) - 1))
        boxes.append(box_pos)
        goals.append(goal_pos)

    # Place player
    player_pos = empty_spaces.pop(randint(0, len(empty_spaces) - 1))

    # Update game map
    for x, y in walls:
        game_map[y][x] = '#'
    for x, y in boxes:
        game_map[y][x] = 'B'
    for x, y in goals:
        game_map[y][x] = 'G'
    game_map[player_pos[1]][player_pos[0]] = 'P'

    return game_map

# Populate the hard level with random walls, boxes, goals, and player
MAPS[2] = [list(row) for row in MAPS[2]]  # Convert strings to mutable lists
MAPS[2] = populate_random_hard_level_with_walls(MAPS[2], num_boxes=21, num_walls=50)  # Add random elements
MAPS[2] = ["".join(row) for row in MAPS[2]]  # Convert lists back to strings


# Calculate screen dimensions dynamically based on the map size
def calculate_screen_size(map_data):
    rows = len(map_data)
    cols = len(map_data[0])
    return cols * TILE_SIZE, rows * TILE_SIZE

# Update WIDTH and HEIGHT dynamically based on the map size
WIDTH, HEIGHT = calculate_screen_size(MAPS[0])

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Box Pushing Game")

# Load images with error handling
try:
    background_image = pygame.image.load('image/sky.jpg')
    wall_image = pygame.image.load('image/wall.png')
    box_image = pygame.image.load('image/crate.png')
    goal_image = pygame.image.load('image/focus.png')
    player_image = pygame.image.load('image/mushroom.png')
    footstep_image = pygame.image.load('image/pawprint.png')

    # Resize images to fit tile size
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
    box_image = pygame.transform.scale(box_image, (TILE_SIZE, TILE_SIZE))
    goal_image = pygame.transform.scale(goal_image, (TILE_SIZE, TILE_SIZE))
    player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
    footstep_image = pygame.transform.scale(footstep_image, (TILE_SIZE, TILE_SIZE))
except pygame.error as e:
    print(f"Error loading image: {e}")
    background_image = None


# Helper functions
def load_map(map_data):
    game_map = []
    boxes = []
    goals = []
    player_pos = None

    for y, row in enumerate(map_data):
        game_row = []
        for x, tile in enumerate(row):
            if tile == 'B':  
                boxes.append((x, y))
                game_row.append(' ')
            elif tile == 'G':  
                goals.append((x, y))
                game_row.append(' ')
            elif tile == 'P':  # Player
                player_pos = (x, y)
                game_row.append(' ')
            else:
                game_row.append(tile)
        game_map.append(game_row)

    return game_map, boxes, goals, player_pos

def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def hill_climbing_path(start, goal, game_map, boxes):
    def is_valid_move(pos):
        x, y = pos
        return (
            0 <= x < len(game_map[0]) and 
            0 <= y < len(game_map) and 
            game_map[y][x] != '#' and 
            pos not in boxes
        )

    current = start
    path = [current]

    while current != goal:
        neighbors = [
            (current[0] + 1, current[1]), 
            (current[0] - 1, current[1]),  
            (current[0], current[1] + 1),  
            (current[0], current[1] - 1)   
        ]

        valid_neighbors = [pos for pos in neighbors if is_valid_move(pos)]
        if not valid_neighbors:
            print(f"No valid moves from {current}")
            return path  

        next_step = min(valid_neighbors, key=lambda pos: heuristic(pos, goal))
        if heuristic(next_step, goal) >= heuristic(current, goal):
            print(f"Stuck at {current}, cannot improve heuristic")
            return path  

        current = next_step
        path.append(current)

    return path

def draw_map(game_map, boxes, goals):
    map_width = len(game_map[0]) * TILE_SIZE
    map_height = len(game_map) * TILE_SIZE
    offset_x = (WIDTH - map_width) // 2
    offset_y = (HEIGHT - map_height) // 2

    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)  # Fallback color if background image is missing

    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            draw_x = offset_x + x * TILE_SIZE
            draw_y = offset_y + y * TILE_SIZE
            if tile == '#':
                screen.blit(wall_image, (draw_x, draw_y))
    for box in boxes:
        draw_x = offset_x + box[0] * TILE_SIZE
        draw_y = offset_y + box[1] * TILE_SIZE
        screen.blit(box_image, (draw_x, draw_y))
    for goal in goals:
        draw_x = offset_x + goal[0] * TILE_SIZE
        draw_y = offset_y + goal[1] * TILE_SIZE
        if goal in boxes:
            pygame.draw.rect(screen, GREEN, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
        else:
            screen.blit(goal_image, (draw_x, draw_y))

def draw_path(path, boxes, goals, game_map, offset_x, offset_y):
    for pos in path:
        x, y = pos
        draw_x = offset_x + x * TILE_SIZE
        draw_y = offset_y + y * TILE_SIZE
        if game_map[y][x] == ' ' and pos not in boxes and pos not in goals:
            screen.blit(footstep_image, (draw_x, draw_y))

def check_win(boxes, goals):
    return all(box in goals for box in boxes)

# def count_boxes_on_goals(boxes, goals):
#     return sum(1 for box in boxes if box in goals)
def count_boxes_on_goals(boxes, goals):
    # Kiểm tra và đếm hộp trên mục tiêu
    count = 0
    for box in boxes:
        if box in goals:
            count += 1
    return count

def display_mode_selection():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Select Mode: P (Player) / A (AI)", True, BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return 'P'
                elif event.key == pygame.K_a:
                    return 'A'

def display_difficulty_selection():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Select Difficulty: 1 (Easy) / 2 (Medium) / 3 (Hard)", True, BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3

def a_star(game_map, start, goal, boxes):
    def is_valid_move(x, y):
        if game_map[y][x] == '#' or (x, y) in boxes:  # Tường hoặc hộp
            return False
        return True

    def heuristic(x, y, goal):
        return abs(x - goal[0]) + abs(y - goal[1])

    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0 + heuristic(start[0], start[1], goal), 0, start))
    came_from = {}

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Đảo ngược đường đi

        closed_list.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in closed_list and is_valid_move(nx, ny):
                new_cost = current_cost + 1
                heapq.heappush(open_list, (new_cost + heuristic(nx, ny, goal), new_cost, (nx, ny)))
                came_from[(nx, ny)] = current

    return []   # Nếu không có đường đi

# Hàm AI Mode sử dụng A*
def ai_mode(game_map, boxes, goals, player_pos):
    print("AI is solving the game...")
    boxes_on_goals = 0

    def find_path_to_goal():
        # Cập nhật thuật toán để tìm hộp gần nhất và di chuyển về đúng mục tiêu
        for box in boxes:
            if box not in goals:
                closest_goal = min([goal for goal in goals if goal not in boxes], key=lambda goal: heuristic(box, goal))
                path = a_star(game_map, box, closest_goal, boxes)  # Tìm đường đi từ box đến goal
                return box, path, closest_goal
        return None, [], None

    while not check_win(boxes, goals):
        box, path, goal = find_path_to_goal()
        if not path:
            print("No solution found by AI.")
            return

        # Vẽ bản đồ hiện tại
        screen.fill(WHITE)
        draw_map(game_map, boxes, goals)

        # Cập nhật số lượng hộp ở mục tiêu
        boxes_on_goals = count_boxes_on_goals(boxes, goals)
        font = pygame.font.Font(None, 36)
        boxes_on_goals_text = font.render(f"Boxes on goals: {boxes_on_goals}/{len(goals)}", True, BLUE)
        total_boxes_text = font.render(f"Total boxes: {len(boxes)}", True, BLUE)
        screen.blit(boxes_on_goals_text, (10, 10))
        screen.blit(total_boxes_text, (10, 50))

        # Vẽ footstep_image theo đường đi của box
        for move in path:
            draw_x, draw_y = move[0] * TILE_SIZE, move[1] * TILE_SIZE
            screen.blit(footstep_image, (draw_x, draw_y))  # Hiển thị dấu chân trên đường đi
            pygame.display.flip()
            pygame.time.wait(200)  # Delay để mô phỏng AI suy nghĩ

            # Cập nhật vị trí player_image để di chuyển cùng với footstep
            player_x, player_y = move[0] * TILE_SIZE, move[1] * TILE_SIZE
            screen.blit(player_image, (player_x, player_y))  # Vẽ player_image tại vị trí mới

        # Di chuyển box đến mục tiêu
        if box:
            # Kiểm tra xem hộp có thể di chuyển đến mục tiêu hợp lệ không
            if game_map[goal[1]][goal[0]] == '#':
                print(f"ERROR: AI tried to move a box into a wall at {goal}")
            elif goal in boxes:
                print(f"ERROR: AI tried to move a box into another box at {goal}")
            else:
                # Cập nhật vị trí của hộp
                boxes[boxes.index(box)] = goal

    # Thông báo AI hoàn thành trò chơi nhưng không dừng ngay lập tức
    print("AI completed the game.")
    screen.fill(WHITE)
    draw_map(game_map, boxes, goals)

    # Hiển thị trạng thái hoàn thành
    boxes_on_goals = count_boxes_on_goals(boxes, goals)
    print(f"Boxes on goals after move: {boxes_on_goals}/{len(goals)}")

    font = pygame.font.Font(None, 74)
    completed_text = font.render("AI completed the map!", True, RED)
    boxes_on_goals_text = font.render(f"Boxes on goals: {boxes_on_goals}/{len(goals)}", True, BLUE)
    screen.blit(completed_text, (WIDTH // 2 - completed_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(boxes_on_goals_text, (WIDTH // 2 - boxes_on_goals_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    # Delay cho người chơi thấy kết quả trước khi kết thúc
    pygame.time.wait(5000) # Hiển thị kết quả trong 2 giây (hoặc thay đổi thời gian)

    # Tiếp tục hoặc thoát (tùy bạn muốn xử lý tiếp theo)


def display_end_game_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    win_text = font.render("You Win!", True, GREEN)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 150))

    option2_text = font.render("2. Select Mode and Map", True, BLUE)
    screen.blit(option2_text, (WIDTH // 2 - option2_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'next'
                elif event.key == pygame.K_2:
                    return 'back'

def run_game():
    while True:
        mode = display_mode_selection()
        difficulty = display_difficulty_selection()
        game_map, boxes, goals, player_pos = load_map(MAPS[difficulty - 1])

        if not player_pos:
            print("Player position not found!")
            return

        if mode == 'P':
            print("Player mode selected.")
        elif mode == 'A':
            ai_mode(game_map, boxes, goals, player_pos)
            option = display_end_game_menu()
            if option == 'back':
                continue
            elif option == 'next':
                difficulty = min(difficulty + 1, len(MAPS))  # Tăng độ khó, tối đa đến level cuối
                continue

        path = []

        map_width = len(game_map[0]) * TILE_SIZE
        map_height = len(game_map) * TILE_SIZE
        offset_x = (WIDTH - map_width) // 2
        offset_y = (HEIGHT - map_height) // 2

        total_boxes = len(boxes)
        total_goals = len(goals)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    new_pos = player_pos
                    if event.key == pygame.K_LEFT:
                        new_pos = (player_pos[0] - 1, player_pos[1])
                    elif event.key == pygame.K_RIGHT:
                        new_pos = (player_pos[0] + 1, player_pos[1])
                    elif event.key == pygame.K_UP:
                        new_pos = (player_pos[0], player_pos[1] - 1)
                    elif event.key == pygame.K_DOWN:
                        new_pos = (player_pos[0], player_pos[1] + 1)

                    if new_pos not in boxes and game_map[new_pos[1]][new_pos[0]] == ' ':
                        player_pos = new_pos

                    elif new_pos in boxes:
                        new_box_pos = (
                            new_pos[0] + (new_pos[0] - player_pos[0]),
                            new_pos[1] + (new_pos[1] - player_pos[1])
                        )
                        if game_map[new_box_pos[1]][new_box_pos[0]] == ' ' and new_box_pos not in boxes:
                            boxes[boxes.index(new_pos)] = new_box_pos
                            player_pos = new_pos

                            if new_box_pos not in goals:
                                closest_goal = min(
                                    [goal for goal in goals if goal not in boxes],
                                    key=lambda goal: heuristic(new_box_pos, goal)
                                )
                                path = a_star(game_map, new_box_pos, closest_goal, boxes)
                            else:
                                path = []

            screen.fill(WHITE)
            draw_map(game_map, boxes, goals)
            if path:
                draw_path(path, boxes, goals, game_map, offset_x, offset_y)

            screen.blit(player_image, (
                offset_x + player_pos[0] * TILE_SIZE,
                offset_y + player_pos[1] * TILE_SIZE
            ))

            font = pygame.font.Font(None, 36)
            boxes_on_goals_text = font.render(f"Boxes on goals: {count_boxes_on_goals(boxes, goals)}", True, GREEN)
            total_boxes_text = font.render(f"Total boxes: {total_boxes}", True, BLUE)
            total_goals_text = font.render(f"Total goals: {total_goals}", True, RED)
            screen.blit(boxes_on_goals_text, (10, 10))
            screen.blit(total_boxes_text, (10, 50))
            screen.blit(total_goals_text, (10, 90))

            if check_win(boxes, goals):
                option = display_end_game_menu()
                if option == 'back':
                    break
                elif option == 'next':
                    difficulty = min(difficulty + 1, len(MAPS))  # Tăng độ khó, tối đa đến level cuối
                    break

            pygame.display.flip()
            pygame.time.Clock().tick(60)


    with open("game_progress.txt", "w") as f:
        f.write(f"Boxes on goals: {count_boxes_on_goals(boxes, goals)}\n")
        f.write(f"Total boxes: {total_boxes}\n")
        f.write(f"Total goals: {total_goals}\n")

run_game()

