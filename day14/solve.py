#!/usr/bin/env python

"""Python solver file for Advent of Code Day 14"""
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
    lookup = {"O": 2, "#": 1, ".": 0}
    return [lookup[x] for x in list(text_line)]


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
    return np.array(data)


def get_load_after_north_tilt(platform):
    """Complete Part 1 work

    Args:
        platform (np.array): grid of values for the rocks

    Returns:
        int: answer to Part 1 question
    """
    platform = platform.copy()
    for c in range(platform.shape[1]):
        for base_r in range(platform.shape[0] - 1):
            # has to be a '.' to be replaceable
            if platform[base_r, c] == 0:
                for check_r in range(base_r + 1, platform.shape[0]):
                    # if you reach a square rock, stop
                    if platform[check_r, c] == 1:
                        break
                    if platform[check_r, c] == 2:
                        # swap and break
                        platform[base_r, c] = 2
                        platform[check_r, c] = 0
                        break

    load = 0
    for r in range(platform.shape[0]):
        load += np.sum(platform[r, :] == 2) * (platform.shape[0] - r)

    return load


def run_spin_cycle(platform):
    """_summary_

    Args:
        platform (_type_): _description_
    """
    # north tilt
    for c in range(platform.shape[1]):
        for base_r in range(platform.shape[0] - 1):
            # has to be a '.' to be replaceable
            if platform[base_r, c] == 0:
                for check_r in range(base_r + 1, platform.shape[0]):
                    # if you reach a square rock, stop
                    if platform[check_r, c] == 1:
                        break
                    if platform[check_r, c] == 2:
                        # swap and break
                        platform[base_r, c] = 2
                        platform[check_r, c] = 0
                        break

    # west
    for r in range(platform.shape[0]):
        for base_c in range(platform.shape[1] - 1):
            # has to be a '.' to be replaceable
            if platform[r, base_c] == 0:
                for check_c in range(base_c + 1, platform.shape[1]):
                    # if you reach a square rock, stop
                    if platform[r, check_c] == 1:
                        break
                    if platform[r, check_c] == 2:
                        # swap and break
                        platform[r, base_c] = 2
                        platform[r, check_c] = 0
                        break
    # south tilt
    for c in range(platform.shape[1]):
        for base_r in range(platform.shape[0] - 1, 0, -1):
            # has to be a '.' to be replaceable
            if platform[base_r, c] == 0:
                for check_r in range(base_r - 1, -1, -1):
                    # if you reach a square rock, stop
                    if platform[check_r, c] == 1:
                        break
                    if platform[check_r, c] == 2:
                        # swap and break
                        platform[base_r, c] = 2
                        platform[check_r, c] = 0
                        break
    # east tilt
    for r in range(platform.shape[0]):
        for base_c in range(platform.shape[1] - 1, 0, -1):
            # has to be a '.' to be replaceable
            if platform[r, base_c] == 0:
                for check_c in range(base_c - 1, -1, -1):
                    # if you reach a square rock, stop
                    if platform[r, check_c] == 1:
                        break
                    if platform[r, check_c] == 2:
                        # swap and break
                        platform[r, base_c] = 2
                        platform[r, check_c] = 0
                        break

    return platform


def get_load(platform):
    """_summary_

    Args:
        platform (_type_): _description_
    """
    load = 0
    for r in range(platform.shape[0]):
        load += np.sum(platform[r, :] == 2) * (platform.shape[0] - r)
    return load


def get_load_after_spin_cycles(platform, cycles=1000000000):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    init_qty = 500
    platform = platform.copy()

    # find pattern
    loads = []
    i = 0
    no_found_repeat = True
    while len(loads) < init_qty and no_found_repeat:
        i_load = get_load(platform)
        logger.debug("load after %d cycles: %d", i, i_load)
        loads.append(i_load)
        i += 1
        platform = run_spin_cycle(platform)

    # find cycle length
    i = 100
    while loads[-i:] != loads[-i * 2 : -i]:
        i += 1

    # at this point, we know the end of the pattern works in multiples of i
    repeat_end = loads[-i:]
    end_value = repeat_end[(cycles - init_qty) % i]
    return end_value


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_load_after_north_tilt(data)
    print(f"Day 14: Part 1: Get Load After North Tilt: {answer}")
    answer2 = get_load_after_spin_cycles(data)
    print(f"Day 14: Part 2: Get Load After 1000000000 Spins: {answer2}")


if __name__ == "__main__":
    main()
