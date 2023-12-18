#!/usr/bin/env python

"""Python solver file for Advent of Code Day 17"""
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
    return [int(x) for x in list(text_line)]


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


def get_least_heat_lost_crucibles(blocks, starting_point=(0, 0), dest_point=(-1, -1)):
    """Complete Part 1

    Args:
        data (np.array): grid representing heat loss amounts for passing through cells
        starting_point (tuple, optional): starting point to work from. Defaults to (0, 0).

    Returns:
        int: minimized heat loss value
    """
    # ensure destination only consists of positive integers
    dest_point = (dest_point[0] % blocks.shape[0], dest_point[1] % blocks.shape[1])

    # queue entries: (point, direction, repeated_steps, heat_lost)
    work_queue = [(starting_point, (0, 1), 0, 0)]
    results = {}
    check_loss_level = 0
    while work_queue:
        next_work_queue_indices = [
            i for i, x in enumerate(work_queue) if x[3] == check_loss_level
        ]
        if not next_work_queue_indices:
            logger.debug("completed loss level: %d...", check_loss_level)
            check_loss_level += 1
            continue
        p, d, r_steps, loss = work_queue.pop(next_work_queue_indices[0])
        entry = (p, d, r_steps)
        if entry in results and results[entry] <= loss:
            # skip doing anything.
            continue
        results[entry] = loss

        # time to add the work for the next steps
        if p == dest_point:
            continue

        possibles = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_d in possibles:
            if new_d == (-d[0], -d[1]):
                continue
            new_p = (p[0] + new_d[0], p[1] + new_d[1])
            r, c = new_p
            if r < 0 or r >= blocks.shape[0] or c < 0 or c >= blocks.shape[1]:
                continue
            new_loss = loss + blocks[new_p]
            if new_d == d:
                if r_steps < 3:
                    new_entry = (new_p, new_d, r_steps + 1, new_loss)
                    if new_entry not in work_queue:
                        work_queue.append(new_entry)
            else:
                new_entry = (new_p, new_d, 1, new_loss)
                if new_entry not in work_queue:
                    work_queue.append(new_entry)

    best_cases = np.zeros(blocks.shape, dtype=int)
    for entry, loss in results.items():
        p = entry[0]
        if best_cases[p] == 0 or best_cases[p] > loss:
            best_cases[p] = loss
    logger.debug("\n %s", best_cases)
    return best_cases[dest_point]


def get_least_heat_loss_ultra_crucibles(
    blocks, starting_point=(0, 0), dest_point=(-1, -1)
):
    """Complete Part 2 work

    Args:
        data (np.array): grid representing heat loss amounts for passing through cells
        starting_point (tuple, optional): starting point to work from. Defaults to (0, 0).

    Returns:
        int: minimized heat loss value
    """
    # ensure destination only consists of positive integers
    dest_point = (dest_point[0] % blocks.shape[0], dest_point[1] % blocks.shape[1])

    # queue entries: (point, direction, repeated_steps, heat_lost)
    work_queue = {0: [(starting_point, (0, 1), 0), (starting_point, (1, 0), 0)]}
    results = {}
    loss = 0
    while work_queue:
        # next_work_queue_indices = [
        #     i for i, x in enumerate(work_queue) if x[3] == check_loss_level
        # ]
        if loss in work_queue and len(work_queue[loss]) == 0:
            del work_queue[loss]
        if loss not in work_queue:
            logger.debug(
                "loss level: %d \t queue size: %s",
                loss,
                len(work_queue.items()),
            )
            loss += 1
            continue
        p, d, r_steps = work_queue[loss].pop()
        entry = (p, d)
        if entry not in results:
            results[entry] = {}
        if r_steps >= 4:
            if r_steps in results[entry] and results[entry][r_steps] < loss:
                # do nothing
                continue
            for check_r in range(r_steps, 11):
                if check_r not in results[entry] or results[entry][check_r] > loss:
                    results[entry][check_r] = loss

        # time to add the work for the next steps
        if p == dest_point:
            continue

        possibles = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_d in possibles:
            if new_d == (-d[0], -d[1]):
                continue
            new_p = (p[0] + new_d[0], p[1] + new_d[1])
            r, c = new_p
            if r < 0 or r >= blocks.shape[0] or c < 0 or c >= blocks.shape[1]:
                continue
            new_loss = loss + blocks[new_p]
            if new_loss not in work_queue:
                work_queue[new_loss] = []
            if new_d == d:
                if r_steps < 10:
                    new_entry = (new_p, new_d, r_steps + 1)
                    if new_entry not in work_queue[new_loss]:
                        work_queue[new_loss].append(new_entry)
            else:
                if r_steps >= 4:
                    new_entry = (new_p, new_d, 1)
                    if new_entry not in work_queue[new_loss]:
                        work_queue[new_loss].append(new_entry)

    best_cases = np.zeros(blocks.shape, dtype=int)
    for entry, lookup in results.items():
        p, _ = entry
        for r_steps, loss in lookup.items():
            if r_steps >= 4:
                if best_cases[p] == 0 or best_cases[p] > loss:
                    best_cases[p] = loss
    best_cases[(0, 0)] = 0
    logger.debug("\n %s", blocks)
    logger.debug("\n %s", best_cases)
    return best_cases[dest_point]


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_least_heat_lost_crucibles(data)
    print(f"Day 17: Part 1: Least Heat Loss for Crucibles (Slow Algo): {answer}")
    answer2 = get_least_heat_loss_ultra_crucibles(data)
    print(f"Day 17: Part 2: Least Heat Loss for Ultra Crucibles (Fast Algo): {answer2}")


if __name__ == "__main__":
    main()
