#!/usr/bin/env python

"""Python solver file for Advent of Code Day 13"""
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
    return [c == "#" for c in list(text_line.strip())]


def parse_pattern(text_pattern):
    """Parses a text blob representing a pattern

    Args:
        text_pattern (str): multiline ASCII grid

    Returns:
        ndarray: grid of True/False value for where the '#' chars are
    """
    data = [
        parse_line(line.strip())
        for line in text_pattern.strip().strip("\n").split("\n")
    ]
    return np.array(data)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    patterns = [
        parse_pattern(blob.strip().strip("\n"))
        for blob in text_data.strip().strip("\n").split("\n\n")
    ]
    return patterns


def get_reflections(pattern):
    """Get the row or col reflections for a given pattern

    Args:
        pattern (np.array): the pattern to search
    Returns:
        (tuple): ([rows], [cols]) where the reflections are found
    """
    rows = []
    cols = []
    for r in range(pattern.shape[0]):
        # handle rows
        if r == 0:
            continue

        if r < (pattern.shape[0] - r):
            size = r
            rev_check = pattern[r - 1 :: -1, :]
        else:
            size = pattern.shape[0] - r
            rev_check = pattern[r - 1 : r - 1 - size : -1, :]

        # logger.debug("checking row %d, size is %d", r, size)
        if np.sum(pattern[r : r + size, :] != rev_check) == 0:
            rows.append(r)
    for c in range(pattern.shape[1]):
        # handle cols
        if c == 0:
            continue

        if c < (pattern.shape[1] - c):
            size = c
            rev_check = pattern[:, c - 1 :: -1]
        else:
            size = pattern.shape[1] - c
            rev_check = pattern[:, c - 1 : c - 1 - size : -1]

        if np.sum(pattern[:, c : c + size] != rev_check) == 0:
            cols.append(c)
    return (rows, cols)


def summarize_reflection_lines(patterns: list):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    row_count = 0
    col_count = 0
    for pattern in patterns:
        rows, cols = get_reflections(pattern)
        row_count += sum(rows)
        col_count += sum(cols)

    return row_count * 100 + col_count


def summarize_smudged_reflection_lines(patterns):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    row_count = 0
    col_count = 0
    for pattern in patterns:
        # get baseline data
        b_rows, b_cols = get_reflections(pattern)
        found_new = False

        # outer loop is iterating through the pattern's points, swapping
        # smudges out and checking for exactly one new reflection
        p = pattern.copy()
        for (r_i, c_i), old_val in np.ndenumerate(p):
            if found_new:
                break
            logger.debug("r_i: %s, c_i: %s, old_val: %s", r_i, c_i, old_val)
            p[r_i, c_i] = not old_val
            check_rows, check_cols = get_reflections(p)
            p[r_i, c_i] = old_val
            for check_row in check_rows:
                if check_row not in b_rows:
                    found_new = True
                    row_count += check_row
            for check_col in check_cols:
                if check_col not in b_cols:
                    found_new = True
                    col_count += check_col

    return row_count * 100 + col_count


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = summarize_reflection_lines(data)
    print(f"Day 13: Part 1: Summation of Reflections: {answer}")
    answer2 = summarize_smudged_reflection_lines(data)
    print(f"Day 13: Part 2: Reflections with Smudges: {answer2}")


if __name__ == "__main__":
    main()
