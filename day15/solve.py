#!/usr/bin/env python

"""Python solver file for Advent of Code Day 15"""
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
    return list(text_line)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    steps = [
        list(text_step.strip())
        for text_step in text_data.strip().strip("\n").split(",")
    ]
    return steps


def get_hash(step):
    """get Holiday ASCII String Helper (HASH)

    Args:
        step (list): list of ASCII chars

    Returns:
        int: HASH value
    """
    value = 0
    for c in step:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def get_steps_hash_sum(steps):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    total = 0
    for step in steps:
        total += get_hash(step)
    return total


def get_lens_index(lenses: list, label: str):
    """Find an existing lens in a list of lens/focal length entries

    Args:
        lenses (list): list of lenses, potentially empty
        key (str): value of the 'lens' field in a dict entry in the list

    Returns:
        int: index of found entry or -1 for not found
    """
    for i, entry in enumerate(lenses):
        if label in entry:
            return i
    return -1


def function2(steps):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    hashmap = {i: [] for i in range(256)}
    for step in steps:
        # denotes a removal
        if step[-1] == "-":
            k = "".join(step[:-1])
            h = get_hash(k)
            box = get_lens_index(hashmap[h], k)
            if box != -1:
                del hashmap[h][box]
        else:
            k, f_l = "".join(step).split("=")
            h = get_hash(k)
            f_l = int(f_l)
            box = get_lens_index(hashmap[h], k)
            if box == -1:
                hashmap[h].append({k: f_l})
            else:
                hashmap[h][box][k] = f_l

    total = 0
    for box in range(256):
        if hashmap[box]:
            for slot, entry in enumerate(hashmap[box]):
                # logger.debug()
                total += (box + 1) * (slot + 1) * list(entry.values())[0]
    return total


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_steps_hash_sum(data)
    print(f"Day 15: Part 1: Hashes: {answer}")
    answer2 = function2(data)
    print(f"Day 15: Part 2: Hashmap: {answer2}")


if __name__ == "__main__":
    main()
