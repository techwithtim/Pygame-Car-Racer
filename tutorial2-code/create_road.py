import random
from operator import mul

PADDING = 50
STARTING_POINT = (0, 0)


def create_path():
    starting_point = STARTING_POINT
    log = []
    current_point = starting_point
    log.append(current_point)

    while True:
        i = random.randint(0, 3)
        match i:
            case 0:  # Up
                current_point = tuple(map(sum, zip(current_point, (0, 1))))

            case 1:  # Down
                current_point = tuple(map(sum, zip(current_point, (0, -1))))
            case 2:  # Left
                current_point = tuple(map(sum, zip(current_point, (-1, 0))))
            case 3:  # Right
                current_point = tuple(map(sum, zip(current_point, (1, 0))))
        if len(log) >= 100:
            # print("RESET", log)
            log = []
            current_point = starting_point
            log.append(current_point)

        elif current_point == starting_point:
            if len(log) <= 8:
                # print("RESET", log)
                log = []
                current_point = starting_point
                log.append(current_point)
            else:
                # log.append(current_point)
                return log
        elif current_point in log:
            log.pop()
            current_point = log[-1]
        else:
            log.append(current_point)


def adjust_path_starting_point_to_fit_screen(path):
    fitted_to_screen_path = []
    minimum_x = 0
    minimum_y = 0
    maximum_x = 0
    maximum_y = 0
    for step_stone in path:
        x, y = step_stone
        if x < minimum_x:
            minimum_x = x
        if y < minimum_y:
            minimum_y = y
        if x > maximum_x:
            maximum_x = x
        if y > maximum_y:
            maximum_y = y

    for step_stone in path:
        step_stone = tuple(map(sum, zip(step_stone, (1 + abs(minimum_x), 1 + abs(minimum_y)))))
        fitted_to_screen_path.append(step_stone)

    starting_position = tuple(map(sum, zip(STARTING_POINT, (PADDING*(1 + abs(minimum_x)), PADDING*(1 + abs(minimum_y))))))
    win_size = (PADDING*(abs(minimum_x) + abs(maximum_x) + 2), PADDING*(abs(minimum_y) + abs(maximum_y) + 2 ))
    return fitted_to_screen_path, starting_position, win_size


def from_path_to_board_coordinates(path):
    on_window_points_coordinates = []
    for step_stone in path:
        on_window_points_coordinates.append(tuple(map(mul, step_stone, (PADDING, PADDING))))
    return on_window_points_coordinates


def from_points_coordinates_to_path_boarders(on_window_points_coordinates):
    path_boarders = []
    bonus_lines = []
    print(on_window_points_coordinates)

    for i in range(-2, len(on_window_points_coordinates) - 2):
        point_a = on_window_points_coordinates[i]
        point_b = on_window_points_coordinates[i+1]
        point_c = on_window_points_coordinates[i+2]
        turn_a = None
        turn_b = None
        if point_a[0] < point_b[0]:
            turn_a = "R"
        elif point_a[0] > point_b[0]:
            turn_a = "L"
        elif point_a[1] > point_b[1]:
            turn_a = "U"
        elif point_a[1] < point_b[1]:
            turn_a = "D"
        else:
            print("im in else,point a and point b:", point_a, point_b)
        if point_b[0] < point_c[0]:
            turn_b = "R"
        elif point_b[0] > point_c[0]:
            turn_b = "L"
        elif point_b[1] > point_c[1]:
            turn_b = "U"
        elif point_b[1] < point_c[1]:
            turn_b = "D"
        else:
            print("im in else,point b and point c:", point_b, point_c)
        if turn_a == turn_b:
            path_boarders += create_tunnel(point_a, turn_a)
        elif turn_a != turn_b:
            path_boarders += create_edge(point_a, turn_a, turn_b)
        if point_a[0] == point_b[0]:
            bonus_line_point_a = (point_a[0] + PADDING/2, (point_a[1] + point_b[1])/2)
            bonus_line_point_b = (point_a[0] - PADDING/2, (point_a[1] + point_b[1])/2)
        else:
            bonus_line_point_a = ((point_a[0] + point_b[0])/2, point_a[1] + PADDING/2)
            bonus_line_point_b = ((point_a[0] + point_b[0])/2, point_a[1] - PADDING/2)
        bonus_lines.append((bonus_line_point_a, bonus_line_point_b))

    return path_boarders, bonus_lines


def main():
    path = create_path()
    adjusted_path, starting_position, win_size = adjust_path_starting_point_to_fit_screen(path)
    points_coordinates = from_path_to_board_coordinates(adjusted_path)
    path_boarders, bonus_lines = from_points_coordinates_to_path_boarders(points_coordinates)
    return path_boarders, bonus_lines, starting_position, win_size


def create_tunnel(starting_position, turn_a):
    boarders_for_edge = []
    border_1 = None
    border_2 = None
    if turn_a == "R":
        border_1 = (tuple(map(sum, zip(starting_position,(PADDING/2,-PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(3 * PADDING/2,-PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (3 * PADDING / 2, PADDING / 2)))))
    elif turn_a == "L":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2,-PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-3 * PADDING/2,-PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (-PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-3 * PADDING / 2, PADDING / 2)))))
    elif turn_a == "U":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2,-PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-PADDING/2,-3*PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (PADDING / 2, -PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (PADDING / 2, -3*PADDING / 2)))))
    elif turn_a == "D":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2,PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-PADDING/2,3*PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (PADDING / 2, 3*PADDING / 2)))))
    boarders_for_edge.append(border_1)
    boarders_for_edge.append(border_2)
    return boarders_for_edge


def create_edge(starting_position, turn_a, turn_b):
    boarders_for_edge = []
    border_1 = None
    border_2 = None
    if turn_a == "R" and turn_b == "D":
        border_1 = (tuple(map(sum, zip(starting_position,(PADDING/2,-PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(3 * PADDING/2,-PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (3 * PADDING / 2, -PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (3* PADDING / 2, PADDING / 2)))))

    elif turn_a == "R" and turn_b == "U":
        border_1 = (tuple(map(sum, zip(starting_position, (PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (3 * PADDING / 2, PADDING / 2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (3 * PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (3 * PADDING / 2, -PADDING / 2)))))

    elif turn_a == "U" and turn_b == "R":
        border_1 = (tuple(map(sum, zip(starting_position, (-PADDING / 2, -PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-PADDING / 2, -3*PADDING / 2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (-PADDING / 2, -3 * PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (PADDING / 2, -3*PADDING / 2)))))
    elif turn_a == "U" and turn_b == "L":
        border_1 = (tuple(map(sum, zip(starting_position, (PADDING / 2, -PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (PADDING / 2, -3*PADDING / 2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (PADDING / 2, -3 * PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-PADDING / 2, -3*PADDING / 2)))))
    elif turn_a == "L" and turn_b == "D":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2,-PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-3 * PADDING/2,-PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (-3 * PADDING / 2, -PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-3 * PADDING / 2, PADDING / 2)))))

    elif turn_a == "L" and turn_b == "U":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2, PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-3 * PADDING/2, PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (-3 * PADDING / 2, PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-3 * PADDING / 2, -PADDING / 2)))))
    elif turn_a == "D" and turn_b == "R":
        border_1 = (tuple(map(sum, zip(starting_position,(-PADDING/2,PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(-PADDING/2, 3* PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (-PADDING / 2,  3*PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (PADDING / 2, 3*PADDING / 2)))))

    elif turn_a == "D" and turn_b == "L":
        border_1 = (tuple(map(sum, zip(starting_position,(PADDING/2,PADDING/2)))),
                    tuple(map(sum, zip(starting_position,(PADDING/2, 3* PADDING/2)))))
        border_2 = (tuple(map(sum, zip(starting_position, (PADDING / 2,  3*PADDING / 2)))),
                    tuple(map(sum, zip(starting_position, (-PADDING / 2, 3*PADDING / 2)))))
    else:
        print("somehow we are on else, turn a turn b", turn_a, turn_b)
    boarders_for_edge.append(border_1)
    boarders_for_edge.append(border_2)
    return boarders_for_edge


if __name__ == '__main__':
    main()
