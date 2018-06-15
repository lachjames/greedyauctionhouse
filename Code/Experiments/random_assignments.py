from Base.auctioneer import Auctioneer
from Base.agent import Agent
from Base.task import Task

from copy import deepcopy

import random

import numpy as np
import scipy.stats as st

from Base.problem_generator import generate_painter

import sys

#X_arg = int(sys.argv[1])

# The X-Y size of our grid of tasks
X = 12

NUM_TESTS = 10
NUM_SPLITS = 20

agents, tasks = generate_painter(X, X, 3)

def main():
    # The probability of running a giveback phase should not be greater than
    # 1 / |Agents|. Otherwise, it will take a VERY long time to finish, and
    # probabilistically might never finish at all!

    # Create a randomly generated schedule and judge it
    s = random_schedule(agents, tasks)

    auctioneer = Auctioneer(None, None, None)
    results = []
    for i in range(100):
        results += [auctioneer.assignment_probability(random_schedule(agents, tasks))]
    mean = np.mean(results)
    # https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
    min_ci, max_ci = st.t.interval(0.95, len(results) - 1, loc=np.mean(results), scale=st.sem(results))
    print(mean, min_ci, max_ci)


def random_schedule(agents, tasks):
    random.shuffle(tasks)
    agent_list = agents * len(tasks)

    schedule = {a: [] for a in agents}
    for t in tasks:
        schedule[agent_list.pop(0)] += [t]

    return schedule

def run_test(pr):
    auctioneer = Auctioneer(deepcopy(agents), deepcopy(tasks), pr)

    schedule = auctioneer.optimize_schedule()
    return auctioneer.assignment_probability(schedule)

s = random_schedule(agents, tasks)
agents[0].print_schedule(X, X, None, s)

#if __name__ == "__main__": main()
