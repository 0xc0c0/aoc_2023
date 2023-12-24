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
    reached = {}
    for r, row in enumerate(tiles):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)

    # entries are (point, step_count)
    work_queue = [(start, 0)]
    completed = {}
    h, w = tiles.shape
    counts = np.zeros(tiles.shape, dtype=int)
    while work_queue:
        cur, step_count = work_queue.pop()
        is_even = step_count % 2 == 0
        lookup_r = cur[0] % h
        lookup_c = cur[1] % w
        if not tiles[(lookup_r, lookup_c)]:
            continue

        if cur not in completed:
            completed[cur] = {}
        # this is where we save the time
        if is_even:
            if "True" not in completed:
                completed[cur][True] = step_count

        if is_even in completed[cur] and completed[cur][is_even] < step_count:
            continue
        completed[cur][is_even] = step_count
        if step_count == steps:
            if (lookup_r, lookup_c) not in reached:
                reached[(lookup_r, lookup_c)] = 1
            else:
                reached[(lookup_r, lookup_c)] += 1
            continue
        for option in [NORTH, SOUTH, EAST, WEST]:
            r = option[0] + cur[0]
            c = option[1] + cur[1]
            if (
                check_bounds((r, c), tiles.shape)
                and (r, c) not in reached
                and step_count < steps
            ):
                work_queue.insert(0, ((r, c), (step_count + 1)))

    logger.debug(reached)
    return sum(list(reached.values()))


def function2(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
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
