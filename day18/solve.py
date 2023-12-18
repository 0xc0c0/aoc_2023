#!/usr/bin/env python

"""Python solver file for Advent of Code Day 18"""
import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_line(text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
    """
    d_lookup = {"R": RIGHT, "D": DOWN, "L": LEFT, "U": UP}
    d_text, n, c_text = text_line.strip().split()
    return (d_lookup[d_text], int(n), c_text.strip("(").strip(")"))


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    dig_plan = [
        parse_line(line.strip()) for line in text_data.strip().strip("\n").split("\n")
    ]
    return dig_plan


def get_turn_offset(d, turn=RIGHT):
    if turn == RIGHT:
        if d == RIGHT:
            return DOWN
        if d == DOWN:
            return LEFT
        if d == LEFT:
            return UP
        if d == UP:
            return RIGHT
    elif turn == LEFT:
        if d == RIGHT:
            return UP
        if d == UP:
            return LEFT
        if d == LEFT:
            return DOWN
        if d == DOWN:
            return RIGHT

    return d


def function(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    right_turns = 0
    p = (0, 0)
    last_d = (0, 0)
    digs = [(p, last_d)]
    for d, n, _ in data:
        if d == get_turn_offset(last_d):
            right_turns += 1
        else:
            right_turns -= 1
        logger.debug(
            "last_d: %s, d: %s, p: %s, right_turns: %d", last_d, d, p, right_turns
        )

        for _ in range(1, n + 1):
            p = (p[0] + d[0], p[1] + d[1])
            digs.append((p, d))

        last_d = d

    points, _ = list(zip(*digs))
    p_rows, p_cols = list(zip(*points))
    size = (max(p_rows) - min(p_rows) + 1, max(p_cols) - min(p_cols) + 1)

    dig_grid = np.zeros(size, dtype=bool)

    logger.debug("\n %s", dig_grid)
    for p, d in digs:
        dig_grid[p] = True

    if right_turns > 0:
        turn = RIGHT
    else:
        turn = LEFT

    for p, d in digs:
        o = get_turn_offset(d, turn=turn)
        logger.debug("p: %s d: %s o: %s", p, d, o)
        inside_p = (p[0] + o[0], p[1] + o[1])
        logger.debug("new_p: %s", inside_p)
        if not dig_grid[inside_p]:
            to_fills = [inside_p]
            while to_fills:
                p1 = to_fills.pop()
                dig_grid[p1] = True
                for d in [UP, DOWN, LEFT, RIGHT]:
                    p2 = (p1[0] + d[0], p1[1] + d[1])
                    if not dig_grid[p2]:
                        to_fills.append(p2)

    return np.sum(dig_grid)


def function2(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    lookup = [RIGHT, DOWN, LEFT, UP]

    instructions = [
        (int(h_text.strip("#")[:5], 16), lookup[int(h_text[-1])])
        for _, _, h_text in data
    ]

    # use this loop to create the sparse matrix and populate the points
    vectors = []
    last_p = (0, 0)
    last_d = (0, 0)
    for n, d in instructions:
        p = (last_p[0] + (d[0] * n), last_p[1] + (d[1] * n))
        vectors.append(((last_p, p), (last_d, d)))
        last_p = p
        last_d = d

    # either sets of points (start and end) will have a complete set of
    # all rows and cols
    points, _ = list(zip(*vectors))
    startps, _ = list(zip(*points))
    p_rows, p_cols = list(zip(*startps))
    sorted_rows = list(set(p_rows))
    tmp = set(sorted_rows)
    for r in tmp:
        if r > 0:
            sorted_rows.append(r - 1)
        sorted_rows.append(r + 1)
    sorted_rows = list(set(sorted_rows))
    sorted_rows.sort()
    logger.debug(sorted_rows)

    sorted_cols = list(set(p_cols))
    tmp = set(sorted_cols)
    for c in tmp:
        if c > 0:
            sorted_cols.append(c - 1)
        sorted_cols.append(c + 1)
    sorted_cols = list(set(sorted_cols))
    sorted_cols.sort()
    logger.debug(sorted_cols)

    size = (len(sorted_rows), len(sorted_cols))
    dig_grid = np.zeros(size, dtype=bool)

    # run through the sparse matrix as in Part 1 to understand which side of
    # the line is the 'inside'
    right_turns = 0
    for points, dirs in vectors:
        last_p, p = points
        last_d, d = dirs

        # count turns to find inside
        if d == get_turn_offset(last_d):
            right_turns += 1
        elif d == get_turn_offset(last_d, turn=LEFT):
            right_turns -= 1

        # get sparse matrix indices
        last_r, last_c = last_p
        r, c = p
        last_s_r = sorted_rows.index(last_r)
        last_s_c = sorted_cols.index(last_c)
        s_r = sorted_rows.index(r)
        s_c = sorted_cols.index(c)

        # mark visited cells along the way
        if last_s_r == s_r:
            for i in range(last_s_c, s_c, d[1]):
                dig_grid[(s_r, i)] = True
        elif last_s_c == s_c:
            for i in range(last_s_r, s_r, d[0]):
                dig_grid[(i, s_c)] = True

    logger.debug("\n %s", dig_grid)
    if right_turns > 0:
        turn = RIGHT
    else:
        turn = LEFT

    for points, dirs in vectors:
        # unpack values
        last_p, p = points
        last_d, d = dirs
        last_r, last_c = last_p
        r, c = p

        # get sparse matrix indices
        last_s_r = sorted_rows.index(last_r)
        last_s_c = sorted_cols.index(last_c)
        s_r = sorted_rows.index(r)
        s_c = sorted_cols.index(c)

        # populate interior cells
        o = get_turn_offset(d, turn=turn)
        logger.debug("turn is %s", turn)
        logger.debug("p: %s d: %s o: %s", p, d, o)
        inside_s_p = (s_r + o[0], s_c + o[1])
        logger.debug("new_p: %s", inside_s_p)
        if not dig_grid[inside_s_p]:
            to_fills = [inside_s_p]
            while to_fills:
                p1 = to_fills.pop()
                dig_grid[p1] = True
                for d in [UP, DOWN, LEFT, RIGHT]:
                    p2 = (p1[0] + d[0], p1[1] + d[1])
                    if not dig_grid[p2]:
                        to_fills.append(p2)

    visual_grid = np.zeros(dig_grid.shape, dtype=int)
    for i, v in np.ndenumerate(dig_grid):
        s_r, s_c = i
        r = sorted_rows[s_r]
        c = sorted_cols[s_c]
        if v:
            h = 0
            w = 0
            if s_r == 0 or not dig_grid[(s_r - 1, s_c)]:
                # if top row or above cell isn't included, then this height is 1
                h = 1
            if s_c == 0 or not dig_grid[(s_r, s_c - 1)]:
                # if left col or lefthand cell isn't included, w is 1
                w = 1
            if h == 0:
                h = r - sorted_rows[s_r - 1]
            if w == 0:
                w = c - sorted_cols[s_c - 1]

            if w != 1 and h != 1:
                # need if this is the case where the upper-left diagonal is empty...
                if not dig_grid[(s_r - 1, s_c - 1)]:
                    visual_grid[i] = h + w - 1
                    continue

            # covers the remainder of the use cases
            visual_grid[i] = h * w

    logger.debug("\n %s", visual_grid)
    return np.sum(visual_grid)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = function(data)
    print(f"Day 18: Part 1: Lava Pool Math: {answer}")
    answer2 = function2(data)
    print(f"Day 18: Part 2: Sparse Matrix Lava Pool Math: {answer2}")


if __name__ == "__main__":
    main()
