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


def get_count_arrangements(arg_springs: list, arg_groupings: list):
    """Determine number of possible arrangements for a row

    Args:
        spring (list): list of springs in order
        grouping (list): list of groupings in order
    """
    arg_entry = (tuple(arg_springs), tuple(arg_groupings))
    work_queue = [arg_entry]
    results = {}
    # completed = 0
    while len(work_queue) != 0:
        # completed += 1
        # if len(work_queue) % 10 == 0:
        #     logger.debug("completed work is: %i", completed)
        springs, groupings = work_queue.pop()
        r_entry = (tuple(springs), tuple(groupings))
        if r_entry not in results:
            results[r_entry] = {"status": "open"}

        if results[r_entry]["status"] == "complete":
            continue

        if results[r_entry]["status"] == "pending":
            check = True
            result_count = 0
            for entry in results[r_entry]["data"]:
                if entry in results and results[entry]["status"] == "complete":
                    result_count += results[entry]["data"]
                else:
                    check = False
                    if r_entry not in work_queue:
                        work_queue.append(r_entry)

            if check is True:
                results[r_entry]["status"] = "complete"
                results[r_entry]["data"] = result_count
                continue

            # did not complete, add to end of queue once all pending runs are done
            work_queue.insert(0, r_entry)
            continue

        logger.debug("attempting %s", (springs, groupings))
        if groupings == tuple():
            results[r_entry]["status"] = "complete"
            if springs.count("#") == 0:
                results[r_entry]["data"] = 1
                continue
            results[r_entry]["data"] = 0
            continue
        if sum(groupings) + len(groupings) - 1 > len(springs):
            results[r_entry]["status"] = "complete"
            results[r_entry]["data"] = 0
            continue  # not possible

        g = groupings[0]
        s = springs[0]
        if s == "#":
            spring_check = springs[:g]
            if spring_check.count(".") > 0:
                results[r_entry]["status"] = "complete"
                results[r_entry]["data"] = 0
                continue
            if len(springs) > g and springs[g] == "#":
                results[r_entry]["status"] = "complete"
                results[r_entry]["data"] = 0
                continue
            # If we're here, it means that the beginning is still valid for the first
            # 'g' number of spring values, including a trailing '.' or '?'
            # This means we assume all are '#' and a trailing '.' and move on
            results[r_entry]["status"] = "pending"
            if r_entry not in work_queue:
                work_queue.append(r_entry)
            opt = (tuple(springs[g + 1 :]), tuple(groupings[1:]))
            results[r_entry]["data"] = [opt]
            work_queue.insert(0, opt)
            continue

        if s == "?":
            if r_entry not in work_queue:
                work_queue.append(r_entry)
            opt1 = (tuple(["."] + list(springs[1:])), tuple(groupings))
            opt2 = (tuple(["#"] + list(springs[1:])), tuple(groupings))
            work_queue.append(opt1)
            work_queue.append(opt2)
            results[r_entry]["status"] = "pending"
            results[r_entry]["data"] = [opt1, opt2]
            continue

        if s == ".":
            if r_entry not in work_queue:
                work_queue.append(r_entry)
            opt = (tuple(springs[1:]), tuple(groupings))
            results[r_entry]["status"] = "pending"
            results[r_entry]["data"] = [opt]
            work_queue.append(opt)
            continue
    logger.debug(results[arg_entry])
    return results[arg_entry]["data"]


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
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_sum_arrangements(data)
    print(f"Day 12: Part 1: Hot Springs Damaged Arrangements: {answer}")
    answer2 = get_expanded_sum_arrangements(data)
    print(f"Day 12: Part 2: Hot Springs Damaged Arrangements: {answer2}")


if __name__ == "__main__":
    main()
