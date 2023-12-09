#!/usr/bin/env python

"""Python solver file for Advent of Code Day 8"""
import os
import math
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
    return list(text_line)


def parse_direction(text_direction):
    """Parse text char containing L or R

    Args:
        text_direction (str): L or R to parse

    Returns:
        int: return 0 or 1 for L or R, respectively
    """
    if text_direction == "L":
        return 0
    elif text_direction == "R":
        return 1


def parse_element(text_element):
    """Parse text element in the form 'AAA = (BBB, CCC)'

    Args:
        text_element (str): text input

    Returns:
        tuple: (node like 'AAA', mapping like ('BBB', 'CCC'))
    """
    text_node, text_mapping = text_element.strip().split(" = ")
    left, right = text_mapping.lstrip("(").rstrip(")").split(", ")
    node = text_node.strip()
    return (node, (left, right))


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    instructions, network_nodes = text_data.strip().strip("\n").split("\n\n")
    instructions = [parse_direction(d) for d in list(instructions.strip())]
    network_nodes = dict(
        [parse_element(text_node) for text_node in network_nodes.strip().split("\n")]
    )
    return instructions, network_nodes


def get_min_required_steps(data, start="AAA", end="ZZZ"):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    instructions, network = data
    loc = start
    count = 0
    passed_start_locs = set()
    while loc != end:
        if loc in passed_start_locs:
            return -1
        passed_start_locs.add(loc)

        for instr in instructions:
            count += 1
            loc = network[loc][instr]
    return count


def check_all_locs(locs):
    """Check if all locations meet the end condition

    Args:
        locs (list): list of locations (e.g. 'AAA')

    Returns:
        bool: True if end conditions met
    """
    for loc in locs:
        if not loc.endswith("Z"):
            return False
    return True


def get_min_required_ghost_steps(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    _, network = data
    starts = [k for k in network.keys() if k.endswith("A")]
    targets = [k for k in network.keys() if k.endswith("Z")]
    steps_tracker = dict()
    for start in starts:
        steps_tracker[start] = set()
        for target in targets:
            logger.debug("next item: %s -> %s", start, target)
            min_steps = get_min_required_steps(data, start, target)
            if min_steps > 0:
                steps_tracker[start].add(min_steps)

    logger.info(steps_tracker)
    # found that there's one path for each start location and one step count

    counts = [e.pop() for _, e in steps_tracker.items()]

    return math.lcm(*counts)

    # brute force method, doesn't work
    # count = 0
    # index = 0
    # while check_all_locs(locs) is False:
    #     logger.info("count is %i, nodes are %s", count, " ".join(locs))

    #     while index != len(locs):
    #         count += 1
    #         instr = instructions[index]
    #         for i, loc in enumerate(locs):
    #             locs[i] = network[loc][instr]
    #         index += 1
    #     index = 0
    # return count


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_min_required_steps(data)
    print(f"Day 8: Part 1: Get Min Required Steps from AAA to ZZZ: {answer}")
    answer2 = get_min_required_ghost_steps(data)
    print(f"Day 8: Part 2: Get Min Required Steps for all Ghost Paths: {answer2}")


if __name__ == "__main__":
    main()
