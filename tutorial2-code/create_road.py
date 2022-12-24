import random
from operator import mul

def create_path():
    starting_point = (0, 0)
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
        if len(log) >= 30:
            print("RESET", log)
            log = []
            current_point = starting_point
            log.append(current_point)

        elif current_point == starting_point:
            if len(log) == 2:
                print("RESET", log)
                log = []
                current_point = starting_point
                log.append(current_point)
            else:
                log.append(current_point)
                return log
        elif current_point in log:
            log.pop()
            current_point = log[-1]
        else:
            log.append(current_point)


def from_path_to_board_coordinates(path):
    board_coordinates = []
    for step_stone in path:
        board_coordinates.append(tuple(map(mul, step_stone, (100, 100))))
    return board_coordinates


def main():
    path = create_path()

    board_coordinates = from_path_to_board_coordinates(path)
    print(board_coordinates)


if __name__ == '__main__':
    main()
