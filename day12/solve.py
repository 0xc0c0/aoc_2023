#!/usr/bin/env python

"""Python solver file for Advent of Code Day 12"""
import os
import logging

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
    text_springs, text_groupings = text_line.split()
    springs = list(text_springs.strip())
    groupings = [int(x) for x in text_groupings.strip().split(",")]
    return springs, groupings


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


def get_count_arrangements(springs: list, groupings):
    """Determine number of possible arrangements for a row

    Args:
        spring (list): list of springs in order
        grouping (list): list of groupings in order
    """
    work_queue = [(springs, groupings)]
    completed = 0
    count = 0
    while len(work_queue) != 0:
        completed += 1
        if len(work_queue) % 10 == 0:
            logger.debug("completed work is: %i", completed)
        springs, groupings = work_queue.pop()
        # logger.debug("attempting %s", (springs, groupings))
        if groupings == []:
            if springs.count("#") == 0:
                # logger.debug("success: %s", springs)
                count += 1  # all must be operational, can't have any damaged
                continue
            continue
        if sum(groupings) + len(groupings) - 1 > len(springs):
            # logger.debug("fail: found too much required parts remaining")
            continue  # not possible

        g = groupings[0]
        s = springs[0]
        if s == "#":
            spring_check = springs[:g]
            if spring_check.count(".") > 0:
                # logger.debug("fail: beginning did not match")
                continue  # not possible
            if len(springs) > g and springs[g] == "#":
                # logger.debug("fail: first grouping too large")
                continue  # not possible
            # If we're here, it means that the beginning is still valid for the first
            # 'g' number of spring values, including a trailing '.' or '?'
            # This means we assume all are '#' and a trailing '.' and move on
            work_queue.append((springs[g + 1 :], groupings[1:]))

        elif s == "?":
            work_queue.append((["."] + springs[1:], groupings))
            work_queue.append((["#"] + springs[1:], groupings))

        elif s == ".":
            work_queue.append((springs[1:], groupings))
    return count


def get_sum_arrangements(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    return sum([get_count_arrangements(*x) for x in data])


def get_expanded_sum_arrangements(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    new_data = [(list("?".join(["".join(s)] * 5)), g * 5) for s, g in data]
    # logger.debug("New Expanded Data is %s", list(new_data))
    return get_sum_arrangements(new_data)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.DEBUG)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_sum_arrangements(data)
    print(f"Day 12: Part 1: <SUMMARY>: {answer}")
    answer2 = get_expanded_sum_arrangements(data)
    print(f"Day 12: Part 2: <SUMMARY>: {answer2}")


if __name__ == "__main__":
    main()
