#!/usr/bin/env python

"""Python solver file for Advent of Code Day 9"""
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    data = [
        [int(x) for x in line.split()]
        for line in text_data.strip().strip("\n").split("\n")
    ]
    return data


def get_extrapolated_value(seq):
    """Analyze the row and get the extrapolated next value

    Args:
        seq (list): sequence of ints
    Returns:
        int: extrapolated next value
    """
    # first, craft the rows
    tmp_seq = seq.copy()
    data = [tmp_seq]
    while tmp_seq.count(0) != len(tmp_seq):
        tmp_seq = [
            tmp_seq[i + 1] - v for i, v in enumerate(tmp_seq[: len(tmp_seq) - 1])
        ]
        data.append(tmp_seq)

    # append the extra 0 on bottom row

    data[-1].append(0)
    for i in range(len(data) - 2, -1, -1):
        # add the end of the row to the end of the extrapolation value of the next row
        data[i].append(data[i][-1] + data[i + 1][-1])

    logger.debug(data)
    return data[0][-1]


def get_prev_extrapolated_value(seq):
    """Analyze the row and get the extrapolated previous value

    Args:
        seq (list): sequence of ints
    Returns:
        int: extrapolated prev value
    """
    # first, craft the rows
    tmp_seq = seq.copy()
    data = [tmp_seq]
    while tmp_seq.count(0) != len(tmp_seq):
        tmp_seq = [
            tmp_seq[i + 1] - v for i, v in enumerate(tmp_seq[: len(tmp_seq) - 1])
        ]
        data.append(tmp_seq)

    # append the extra 0 on bottom row

    data[-1].insert(0, 0)
    for i in range(len(data) - 2, -1, -1):
        # add the end of the row to the end of the extrapolation value of the next row
        data[i].insert(0, data[i][0] - data[i + 1][0])

    logger.debug(data)
    return data[0][0]


def find_extrapolation_sum(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    return sum([get_extrapolated_value(seq) for seq in data])


def find_extrapolation_prev_sum(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    return sum([get_prev_extrapolated_value(seq) for seq in data])


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = find_extrapolation_sum(data)
    print(f"Day 9: Part 1: Sum of All Extrapolated Next Values: {answer}")
    answer2 = find_extrapolation_prev_sum(data)
    print(f"Day 9: Part 2: Sum of All Extrapolated Prev Values: {answer2}")


if __name__ == "__main__":
    main()
