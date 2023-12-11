#!/usr/bin/env python

"""Python solver file for Advent of Code Day 11"""
import os
import logging
import itertools
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
    return [c == "#" for c in list(text_line)]


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
    galaxies = np.array(data)
    # logger.debug(galaxies)
    # logger.debug(galaxies.shape)
    return galaxies


def get_sum_galaxy_distances(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    data = data.copy()
    for r in range(data.shape[0] - 1, -1, -1):
        if (data[r, :]).sum() == 0:
            data = np.insert(data, r, False, axis=0)

    for c in range(data.shape[1] - 1, -1, -1):
        if (data[:, c]).sum() == 0:
            logger.debug("inserting at column %d", c)
            data = np.insert(data, c, False, axis=1)

    pairs = itertools.combinations(np.argwhere(data == True), 2)
    distances = [abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in pairs]

    return sum(distances)


def get_sum_galaxy_distances_multiple(data, expansion_mult=1000000):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    data = data.copy()
    expansion_rows = list()
    for r in range(data.shape[0] - 1, -1, -1):
        if (data[r, :]).sum() == 0:
            expansion_rows.append(r)
    expansion_rows = np.array(expansion_rows)

    expansion_cols = list()
    for c in range(data.shape[1] - 1, -1, -1):
        if (data[:, c]).sum() == 0:
            expansion_cols.append(c)
    expansion_cols = np.array(expansion_cols)

    galaxy_indices = np.argwhere(data == True)
    expanded_galaxy_indices = list()
    for i in galaxy_indices:
        r, c = i
        new_r = r + ((expansion_rows < r).sum() * (expansion_mult - 1))
        new_c = c + ((expansion_cols < c).sum() * (expansion_mult - 1))
        logger.debug("%s became %s", i, (new_r, new_c))
        expanded_galaxy_indices.append((new_r, new_c))

    pairs = itertools.combinations(expanded_galaxy_indices, 2)
    distances = [abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in pairs]

    return sum(distances)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_sum_galaxy_distances(data)
    print(f"Day 11: Part 1: Find Galaxy Distances With Doubling : {answer}")
    answer2 = get_sum_galaxy_distances_multiple(data)
    print(f"Day 11: Part 2: Find Galaxy Distances With x1,000,000: {answer2}")


if __name__ == "__main__":
    main()
