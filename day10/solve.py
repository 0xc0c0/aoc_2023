#!/usr/bin/env python

"""Python solver file for Advent of Code Day 10"""
import os
import logging
import sys
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

sys.setrecursionlimit(2000)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_char(char):
    """Translate ASCII art pipe into coordinate delta for each end of pipe

    Args:
        char (str): ASCII char

    Returns:
        list: None, [], or tuple pairs of coordinate offsets representing the pipe
    """
    lookup = {
        "S": [],
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "7": [(0, -1), (1, 0)],
        "F": [(1, 0), (0, 1)],
        ".": None,
    }
    return lookup[char]


def get_side_tiles(entrance_vector, pipe_info):
    """Get the offsets to the lefthand and righthand tiles

    Args:
        entrance_vector (tuple): tuple or list with the vector used to get to the tile
        point (list): tile's stored pipe info (offsets to tiles where the pipe is connected)

    Returns:
        dict: lefthand tile list as 'left' and right tile list as 'right'
    """
    localp = pipe_info.copy()

    # entered from the west
    if entrance_vector == (0, 1):
        localp.remove((0, -1))
        outbound_dir = localp.pop()
        # heading north
        if outbound_dir == (-1, 0):
            return {"left": [], "right": [(1, 0), (0, 1)], "turn": -1}
        # heading east
        if outbound_dir == (0, 1):
            return {"left": [(-1, 0)], "right": [(1, 0)], "turn": 0}
        # heading south
        if outbound_dir == (1, 0):
            return {"left": [(-1, 0), (0, 1)], "right": [], "turn": 1}

    # entered from the east
    if entrance_vector == (0, -1):
        localp.remove((0, 1))
        outbound_dir = localp.pop()
        # heading north
        if outbound_dir == (-1, 0):
            return {"left": [(1, 0), (0, -1)], "right": [], "turn": 1}
        # heading west
        if outbound_dir == (0, -1):
            return {"left": [(1, 0)], "right": [(-1, 0)], "turn": 0}
        # heading south
        if outbound_dir == (1, 0):
            return {"left": [], "right": [(-1, 0), (0, -1)], "turn": -1}

    # entered from the north
    if entrance_vector == (1, 0):
        localp.remove((-1, 0))
        outbound_dir = localp.pop()
        # heading east
        if outbound_dir == (0, 1):
            return {"left": [], "right": [(0, -1), (1, 0)], "turn": -1}
        # heading west
        if outbound_dir == (0, -1):
            return {"left": [(0, 1), (1, 0)], "right": [], "turn": 1}
        # heading south
        if outbound_dir == (1, 0):
            return {"left": [(0, 1)], "right": [(0, -1)], "turn": 0}

    # entered from the south
    if entrance_vector == (-1, 0):
        localp.remove((1, 0))
        outbound_dir = localp.pop()
        # heading north
        if outbound_dir == (-1, 0):
            return {"left": [(0, -1)], "right": [(0, 1)], "turn": 0}
        # heading west
        if outbound_dir == (0, -1):
            return {"left": [], "right": [(-1, 0), (0, 1)], "turn": -1}
        # heading east
        if outbound_dir == (0, 1):
            return {"left": [(-1, 0), (0, -1)], "right": [], "turn": 1}

    # should never happen
    logger.info("should never get here!")
    return None


def mark_adjacent_ground_tiles(grid, p, value):
    """mark tile and everything around it

    Args:
        grid (np.ndarray): matrix the size of data representing knowledge about the tile
        p (tuple): coordinates of point
        value (int): value to make the point and surrounding points
    """
    # make sure the point is valid
    if 0 <= p[0] < grid.shape[0] and 0 <= p[1] < grid.shape[1]:
        # if unmarked, mark it and try to mark everything around it
        if grid[p] == 0 or grid[p] == 1:
            grid[p] = value
            if p[0] != 0:  # not top row
                mark_adjacent_ground_tiles(grid, (p[0] - 1, p[1]), value)
            if p[0] != (grid.shape[0] - 1):  # not bottom row
                mark_adjacent_ground_tiles(grid, (p[0] + 1, p[1]), value)
            if p[1] != 0:  # not leftmost column
                mark_adjacent_ground_tiles(grid, (p[0], p[1] - 1), value)
            if p[1] != (grid.shape[1] - 1):
                mark_adjacent_ground_tiles(grid, (p[0], p[1] + 1), value)


def parse_line(text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
    """
    return [parse_char(c) for c in list(text_line.strip())]


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    data = [
        parse_line(line.strip()) for line in text_data.strip().strip("\n").split("\n")
    ]

    return data


def function(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    # find S
    start = None
    for r, row in enumerate(data):
        for c, entry in enumerate(row):
            if entry == []:
                start = (r, c)
                break
        if start:
            break

    # get connected starting directions from S, by looking at all surrounding
    # cells and seeing which of them have pipes leading to S
    possibilites = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if start[0] == 0:
        possibilites.remove((-1, 0))
    if start[0] == len(data) - 1:
        possibilites.remove((1, 0))
    if start[1] == 0:
        possibilites.remove((0, -1))
    if start[1] == len(data[0]) - 1:
        possibilites.remove((0, 1))

    logger.debug(start)
    logger.debug(possibilites)

    # populate start's connections/pipe
    for o in possibilites:
        # check if the possibility has a pipe connection to S
        p_data = data[start[0] + o[0]][start[1] + o[1]]
        backward_check = (o[0] * -1, o[1] * -1)
        if p_data is None:
            continue
        if backward_check in p_data:
            # add pipe connection to S
            data[start[0]][start[1]].append(o)

    logger.debug(data[start[0]][start[1]])

    # pick first pipe connection from S to begin counting
    step_count = 1
    last_point = start
    last_offset = data[start[0]][start[1]][0]
    cur_point = (last_point[0] + last_offset[0], last_point[1] + last_offset[1])
    while cur_point != start:
        # get first next_point option
        p1, p2 = data[cur_point[0]][cur_point[1]]
        o = p1
        backward_check = (o[0] * -1, o[1] * -1)
        if backward_check == last_offset:
            o = p2

        # progress step
        step_count += 1
        last_point = cur_point
        last_offset = o
        cur_point = (last_point[0] + last_offset[0], last_point[1] + last_offset[1])

    return int(step_count / 2)


def get_enclosed_tile_count(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    # find S
    start = None
    for r, row in enumerate(data):
        for c, entry in enumerate(row):
            if entry == []:
                start = (r, c)
                break
        if start:
            break

    # get connected starting directions from S, by looking at all surrounding
    # cells and seeing which of them have pipes leading to S
    possibilites = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if start[0] == 0:
        possibilites.remove((-1, 0))
    if start[0] == len(data) - 1:
        possibilites.remove((1, 0))
    if start[1] == 0:
        possibilites.remove((0, -1))
    if start[1] == len(data[0]) - 1:
        possibilites.remove((0, 1))

    logger.debug(start)
    logger.debug(possibilites)

    # populate start's connections/pipe
    for o in possibilites:
        # check if the possibility has a pipe connection to S
        p_data = data[start[0] + o[0]][start[1] + o[1]]
        backward_check = (o[0] * -1, o[1] * -1)
        if p_data is None:
            continue
        if backward_check in p_data:
            # add pipe connection to S
            data[start[0]][start[1]].append(o)

    logger.debug(data[start[0]][start[1]])

    # used a new grid of the right size to figure out and track inside vs. outside
    # 0 = unknown
    # 1 = pipe
    # 2 = lefthand ground tile
    # 3 = righthand ground tile
    # 4 = loop path pipe
    grid = np.zeros((len(data), len(data[0])), dtype=int)
    for r, row in enumerate(data):
        for c, entry in enumerate(row):
            if entry is not None:
                grid[r, c] = 1

    # first, run the circuit to mark the loop pipe
    last_point = start
    last_offset = data[start[0]][start[1]][0]
    cur_point = (last_point[0] + last_offset[0], last_point[1] + last_offset[1])
    while cur_point != start:
        grid[cur_point] = 4

        # get first next_point option
        p1, p2 = data[cur_point[0]][cur_point[1]]
        o = p1
        backward_check = (o[0] * -1, o[1] * -1)
        if backward_check == last_offset:
            o = p2

        # progress step
        last_point = cur_point
        last_offset = o
        cur_point = (cur_point[0] + o[0], cur_point[1] + o[1])

    # figure out whether left or right is the inside in the direction of propagation
    last_point = start
    last_offset = data[start[0]][start[1]][0]
    cur_point = (last_point[0] + last_offset[0], last_point[1] + last_offset[1])
    grid[last_point] = 4
    turn_count = 0
    while cur_point != start:
        # get first next_point option
        p1, p2 = data[cur_point[0]][cur_point[1]]
        o = p1
        backward_check = (o[0] * -1, o[1] * -1)
        if backward_check == last_offset:
            o = p2

        # get lefthand and righthand tiles
        side_tiles = get_side_tiles(last_offset, [p1, p2])
        turn_count += side_tiles["turn"]

        # mark all connected lefthand and righthand tiles
        for offset in side_tiles["left"]:
            p = (cur_point[0] + offset[0], cur_point[1] + offset[1])
            mark_adjacent_ground_tiles(grid, p, 2)
        for offset in side_tiles["right"]:
            p = (cur_point[0] + offset[0], cur_point[1] + offset[1])
            mark_adjacent_ground_tiles(grid, p, 3)

        # progress step
        last_point = cur_point
        last_offset = o
        cur_point = (cur_point[0] + o[0], cur_point[1] + o[1])

    np.savetxt("grid.txt", grid, fmt="%d")
    # analyze grid to see whether left or right is the 'inside' side
    if turn_count > 0:  # more righthand turns... righthand is inside
        logger.debug("inside is the righthand side")
        return (grid == 3).sum()

    # lefthand is inside
    logger.debug("inside is the lefthand side")
    return (grid == 2).sum()


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = function(data)
    print(f"Day 10: Part 1: Find Step Count For Furthest Away Pipe: {answer}")
    data = parse_data(text_data)
    answer2 = get_enclosed_tile_count(data)
    print(f"Day 10: Part 2: Find Number of Tiles Enclosed by Pipe Loop: {answer2}")


if __name__ == "__main__":
    main()
