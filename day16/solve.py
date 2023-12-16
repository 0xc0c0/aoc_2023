#!/usr/bin/env python

"""Python solver file for Advent of Code Day 16"""
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
    return list(text_line)


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
    return np.array(data, dtype=str)


def get_energized_sum(data: np.array, init=(0, 0, (0, 1))):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    energized_grid = np.zeros(data.shape, dtype=bool)
    energizing_queue = [init]
    done_flows = []
    while energizing_queue:
        flow = energizing_queue.pop()
        logger.debug("starting %s", flow)
        if flow in done_flows:
            continue
        r, c, d = flow
        while True:
            # evaluate space
            if r < 0 or r >= data.shape[0] or c < 0 or c >= data.shape[1]:
                done_flows.append(flow)
                break
            energized_grid[r, c] = True
            val = data[r, c]
            # dots, or entering ends of | or -
            if val == ".":
                r += d[0]
                c += d[1]
            elif (val == "-" and d[0] == 0) or (val == "|" and d[1] == 0):
                # call this flow done, and start a new one
                done_flows.append(flow)
                energizing_queue.append((r + d[0], c + d[1], d))
                break
            elif val == "/":
                done_flows.append(flow)
                d = (-d[1], -d[0])  # 90 degree turn
                energizing_queue.append((r + d[0], c + d[1], d))
                break
            elif val == "\\":
                done_flows.append(flow)
                d = (d[1], d[0])
                energizing_queue.append((r + d[0], c + d[1], d))
                break
            elif val == "|" or val == "-":
                done_flows.append(flow)
                d1 = (d[1], d[0])
                d2 = (-d[1], -d[0])
                energizing_queue.append((r + d1[0], c + d1[1], d1))
                energizing_queue.append((r + d2[0], c + d2[1], d2))
                break

    return np.sum(energized_grid)


def check_all_entrances_for_max(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    # craft initial vectors
    from_left = [(r, 0, (0, 1)) for r in range(data.shape[0])]
    from_top = [(0, c, (1, 0)) for c in range(data.shape[1])]
    from_right = [
        (r, data.shape[1] - 1, (0, -1)) for r in range(data.shape[0] - 1, -1, -1)
    ]
    from_bottom = [
        (data.shape[0] - 1, c, (-1, 0)) for c in range(data.shape[1] - 1, -1, -1)
    ]
    all_entrances = from_left + from_top + from_right + from_bottom

    max_tiles = 0
    for entrance in all_entrances:
        tiles = get_energized_sum(data, entrance)
        if tiles > max_tiles:
            max_tiles = tiles
    return max_tiles


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_energized_sum(data)
    print(f"Day 16: Part 1: Get Energized Tiles: {answer}")
    answer2 = check_all_entrances_for_max(data)
    print(f"Day 16: Part 2: Get Max Energized Tiles: {answer2}")


if __name__ == "__main__":
    main()
