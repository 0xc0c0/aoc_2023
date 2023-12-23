#!/usr/bin/env python

"""Python solver file for Advent of Code Day 20"""
import os
import logging
import math

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
    text_tx, text_rxs = text_line.strip().split(" -> ")
    text_tx = text_tx.strip()
    if text_tx == "broadcaster":
        op = "broadcast"
        name = "broadcaster"
    else:
        op = text_tx[0]
        name = text_tx[1:]

    state = 0
    rxs = text_rxs.strip().split(", ")
    # state only really matters for flip-flops
    return (name, {"op": op, "rxs": rxs, "mem": {}, "state": state})


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    modules = [
        parse_line(line.strip()) for line in text_data.strip().strip("\n").split("\n")
    ]
    modules = {k: v for k, v in modules}
    for name, m in modules.items():
        inputs = [
            check_n for check_n, check_m in modules.items() if name in check_m["rxs"]
        ]
        for name in inputs:
            m["mem"][name] = 0
        logger.debug("name: %s, module: %s", name, m)
    # for name, m in modules.items():
    #     for rx in m["rxs"]:
    #         if rx not in modules:
    #             modules[rx] = {"op": None, "rxs": None, "state": 0, "mem": {}}
    return modules


def function(modules, rounds=1000):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    low_pulses = 0
    high_pulses = 0
    for i in range(rounds):
        # fire pulse
        next_work_queue = [(None, "broadcaster", 0)]

        while next_work_queue:
            work_queue = next_work_queue
            next_work_queue = []
            while work_queue:
                src, name, signal = work_queue.pop()
                if signal:
                    high_pulses += 1
                else:
                    low_pulses += 1
                if name not in modules:
                    continue
                m = modules[name]
                # logger.debug("name: %s, m: %s", name, m)
                if m["op"] == "broadcast":
                    for rx in m["rxs"]:
                        # logger.debug((name, rx, signal))
                        next_work_queue.insert(0, (name, rx, signal))
                elif m["op"] == "%":
                    if signal == 0:
                        # logger.debug((name, m["state"]))
                        m["state"] = 1 if m["state"] == 0 else 0
                        for rx in m["rxs"]:
                            next_work_queue.insert(0, (name, rx, m["state"]))
                            # logger.debug((name, rx, m["state"]))
                elif m["op"] == "&":
                    m["mem"][src] = signal
                    send = 0
                    for val in m["mem"].values():
                        if val == 0:
                            send = 1
                            break
                    for rx in m["rxs"]:
                        next_work_queue.insert(0, (name, rx, send))
                        # logger.debug((name, rx, send))
                else:
                    logger.debug("should never get here")

        # logger.debug(
        #     "round %d complete :: low: %d, high: %d", i + 1, low_pulses, high_pulses
        # )

    return low_pulses * high_pulses


def get_pulse_counts(modules, rounds=1):
    low_pulses = {k: 0 for k in modules.keys()}
    low_pulses["rx"] = 0
    high_pulses = {k: 0 for k in modules.keys()}
    high_pulses["rx"] = 0
    for _ in range(rounds):
        # fire pulse
        next_work_queue = [(None, "broadcaster", 0)]

        while next_work_queue:
            work_queue = next_work_queue
            next_work_queue = []
            while work_queue:
                src, name, signal = work_queue.pop()
                if signal == 0:
                    low_pulses[name] += 1
                elif signal == 1:
                    high_pulses[name] += 1
                if name not in modules:
                    continue
                m = modules[name]
                # logger.debug("name: %s, m: %s", name, m)
                if m["op"] == "broadcast":
                    for rx in m["rxs"]:
                        # logger.debug((name, rx, signal))
                        next_work_queue.insert(0, (name, rx, signal))
                elif m["op"] == "%":
                    if signal == 0:
                        # logger.debug((name, m["state"]))
                        m["state"] = 1 if m["state"] == 0 else 0
                        for rx in m["rxs"]:
                            next_work_queue.insert(0, (name, rx, m["state"]))
                            # logger.debug((name, rx, m["state"]))
                elif m["op"] == "&":
                    m["mem"][src] = signal
                    send = 0
                    for val in m["mem"].values():
                        if val == 0:
                            send = 1
                            break
                    for rx in m["rxs"]:
                        next_work_queue.insert(0, (name, rx, send))
                        # logger.debug((name, rx, send))
                else:
                    logger.debug("should never get here")

        # logger.debug(
        #     "round %d complete :: low: %d, high: %d", i + 1, low_pulses, high_pulses
        # )

    return low_pulses, high_pulses


def print_deps_node(modules, node_name):
    if node_name in modules:
        outputs = modules[node_name]["rxs"]
        print(f"{outputs} <- {modules[node_name]['state']} - {node_name}")
        inputs = [f"{rx}:{state}" for rx, state in modules[node_name]["mem"].items()]
        print(f"\t {node_name} <- {modules[node_name]['op']} - {inputs}")


def sort_val(e):
    return e[2]


def print_deps_tree(modules, start="rx", flip_flops=None):
    start_deps = [name for name in modules if start in modules[name]["rxs"]]
    s1 = start_deps[0]
    logger.debug(f"{start} <- {s1}:{modules[s1]['state']}")
    work_queue = start_deps
    printed = []
    while work_queue:
        cur = work_queue.pop()
        if cur not in printed:
            mem_data = list(modules[cur]["mem"].items())
            if flip_flops:
                sorted_list = [
                    (rx, state, flip_flops[rx]["period"] if rx in flip_flops else 0)
                    for rx, state in mem_data
                ]
                sorted_list.sort(key=sort_val)
                mem_data = [(rx, state) for rx, state, _ in sorted_list]
            key_values = [f"{rx}:{state}" for rx, state in mem_data]

            logger.debug(f"{cur} {modules[cur]['op']} <- {key_values}")
            printed.append(cur)
        for c in modules[cur]["mem"].keys():
            if c not in printed:
                work_queue.insert(0, c)


def init_modules(modules):
    for _, m in modules.items():
        m["state"] = 0
        for x in m["mem"]:
            m["mem"][x] = 0


def function2(modules):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    # find flip flops patterns
    # dict entries: o is offset to first '1' value and 'r' is freq between repeats
    flip_flops = {}
    concerns = ["vm", "kb", "dn", "vk"]
    for name, m in modules.items():
        if m["op"] == "%":
            for concern in concerns:
                if name in modules[concern]["mem"].keys():
                    flip_flops[name] = {"offset": 0, "period": 0, "pattern": []}

    init_modules(modules)
    rounds = 0
    for _ in range(100000):
        low, high = get_pulse_counts(modules, 1)
        rounds += 1
        for name, ff in flip_flops.items():
            if modules[name]["state"] == 1:
                # if ff["period"] == 0:
                ff["pattern"].append(rounds)
                # if len(ff["pattern"]) >= 4:
                #     logger.debug("%s : %s", name, ff["pattern"])

    for name, ff in flip_flops.items():
        pattern = ff["pattern"].copy()
        ff["offset"] = pattern[0]
        high_count = 1
        last_num = pattern.pop()
        last_diff = 1
        guess_low_count = 0
        guess_high_count = 0
        while ff["period"] == 0:
            num = pattern.pop()
            diff = last_num - num
            if diff == 1:
                high_count += 1
            else:
                if guess_low_count == diff:
                    ff["period"] = guess_low_count
                    logger.debug(
                        "name: %s, value: %d, diff: %d, last_num: %d, num: %d",
                        name,
                        num,
                        diff,
                        last_num,
                        num,
                    )
                else:
                    logger.debug(
                        "name: %s, value: %d, diff: %d, last_num: %d, num: %d",
                        name,
                        num,
                        diff,
                        last_num,
                        num,
                    )
                    guess_low_count = diff
                    guess_high_count = high_count
                high_count = 1

            last_num = num
            last_diff = diff

    for name, ff in flip_flops.items():
        logger.debug(
            "%s :: offset: %d, period: %d, pattern: %s",
            name,
            ff["offset"],
            ff["period"],
            ff["pattern"][-16:],
        )

    # pick a module and go deep on how its repetition works

    init_modules(modules)
    # for concern in concerns:
    #     for n in modules[concern]["mem"]:
    #         modules[concern]["mem"][n] = 1

    print_deps_tree(modules, flip_flops=flip_flops)
    rounds = 0
    concerns = ["fv", "kk", "vt", "xr"]
    offsets = []
    while concerns:
        low, high = get_pulse_counts(modules, 1)
        rounds += 1
        if low["rx"] > 0:
            return rounds

        for c in concerns:
            if low[c] > 0:
                logger.debug("%s low pulsed after %d pushes", c, rounds)
                concerns.remove(c)
                offsets.append(rounds)
                # logger.debug(
                #     "rx :: high count: %d, low count: %d", high["rx"], low["rx"]
                # )
                # print_deps_tree(modules, flip_flops=flip_flops)
                # logger.debug("LOW: \n %s", low)
                # logger.debug("HIGH: \n %s", high)
                break

    return math.lcm(*offsets)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = function(data)
    print(f"Day 20: Part 1: Gate Logic - 1000 Rounds: {answer}")
    answer2 = function2(data)
    print(f"Day 20: Part 2: Gate Logic - Reversing input.txt: {answer2}")


if __name__ == "__main__":
    main()
