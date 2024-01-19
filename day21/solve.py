#!/usr/bin/env python

"""Python solver file for Advent of Code Day 21"""
import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


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
    start = -1
    line = [c in (".", "S") for c in text_line.strip()]
    if "S" in text_line:
        start = text_line.index("S")
    return line, start


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    start = (0, 0)
    data = []
    for r, line in enumerate(text_data.strip().strip("\n").split("\n")):
        row, c = parse_line(line.strip())
        if c != -1:
            start = (r, c)
        data.append(row)
    return np.array(data), start


NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)


def check_bounds(point, dim):
    r, c = point
    if 0 <= r < dim[0] and 0 <= c < dim[1]:
        return True
    return False


def function(tiles, start, steps=64):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    reached = np.zeros((len(tiles), len(tiles[0])), dtype=bool)
    for r, row in enumerate(tiles):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)

    # entries are (point, step_count)
    work_queue = [(start, 0)]
    completed = {}
    while work_queue:
        cur, step_count = work_queue.pop()
        is_even = step_count % 2 == 0
        if not tiles[cur]:
            continue
        if cur not in completed:
            completed[cur] = {}
        if is_even in completed[cur] and completed[cur][is_even] >= step_count:
            continue

        completed[cur][is_even] = step_count
        if step_count == steps:
            reached[cur] = True
            continue
        for option in [NORTH, SOUTH, EAST, WEST]:
            r = option[0] + cur[0]
            c = option[1] + cur[1]
            if check_bounds((r, c), tiles.shape) and not reached[(r, c)]:
                work_queue.insert(0, ((r, c), (step_count + 1)))

    logger.debug(reached)
    return np.sum(reached)


def function2(tiles, start=None, steps=6):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    # default to center square
    if not start:
        start = (size // 2, size // 2)

    # guaranteed completed square
    full_step_count = size * 2

    # assumes square
    size = tiles.shape[0]

    running_total = 0

    memo = {}
    
    ROOT = 3
    TRUNK = 4
    BRANCH = 5
    
    # Algorithm/approach
    #         ^
    #       < | ^
    #     < < | ^ ^
    #   < < < | ^ ^ ^
    # <-------o-------> 
    #   v v v | > > >
    #     v v | > > --- branches continue in one direction only
    #       v | > 
    #         v --- trunks spawn new branches 90 deg counterclockwise

    ring = 0
    work_queue = [('root', start, steps)]
    while work_queue:
        ring, s, rem_steps = work_queue.pop()
        if ring == 0:
            # need to setup trunks in all directions

    return 0


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = function(*data)
    print(f"Day 21: Part 1: <SUMMARY>: {answer}")
    answer2 = function2(data)
    print(f"Day 21: Part 2: <SUMMARY>: {answer2}")


if __name__ == "__main__":
    main()
