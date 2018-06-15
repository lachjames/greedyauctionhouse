# https://stackoverflow.com/questions/6323860/sibling-package-imports

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from Base.annealing import Annealer
from Base.agent import Agent
from Base.task import Task

from Base.problem_generator import generate_painter
from copy import deepcopy

import numpy as np
import scipy.stats as st

import yaml

import timeit
import itertools

# Reference: https://sebastianraschka.com/Articles/2014_multiprocessing.html
# and http://kmdouglass.github.io/posts/learning-pythons-multiprocessing-module.html
import multiprocessing as mp

# The X-Y size of our grid of tasks
#X = 12
#Y = 12

NUM_PROCESSES = mp.cpu_count() - 1
print(NUM_PROCESSES, "threads at once!")

# Import settings
with open("annealer_settings.yaml", "r") as f:
    parameters = yaml.load(f)

print(parameters)

def one_temp(start_temp, agents, tasks):
    pool = mp.Pool(processes=NUM_PROCESSES)
    results_and_times = pool.starmap(
       run_test,
       ((start_temp, deepcopy(agents), deepcopy(tasks)) for _ in range(parameters["num_experiments"]))
    )
    pool.close()
    # results_and_times = itertools.starmap(
    #     run_test,
    #     ((start_temp, deepcopy(agents), deepcopy(tasks)) for _ in range(parameters["num_experiments"]))
    # )

    results, times = zip(*results_and_times)

    mean = np.mean(results)
    mean_time = np.mean(times)
    # https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
    min_ci, max_ci = st.t.interval(0.95, len(results) - 1, loc=np.mean(results), scale=st.sem(results))

    #print(mean)
    #print(min_ci, max_ci)

    #output.put((mean, min_ci, max_ci))
    return (mean, min_ci, max_ci, mean_time)

def one_X(X):
    Y = X
    agents, tasks = generate_painter(X, Y, parameters["num_agents"])

    # https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
    results = []
    temps = eval(parameters["temps"])
    for t in temps:
        results += [one_temp(t, agents, tasks)]
    # https://stackoverflow.com/questions/12974474/how-to-unzip-a-list-of-tuples-into-individual-lists
    means, min_cis, max_cis, mean_times = zip(*results)

    with open("anneal_data/{}.csv".format(X), "w") as f:
        for i in range(len(temps)):
            f.write("{},{},{},{},{}\n".format(temps[i], means[i], min_cis[i], max_cis[i], mean_times[i]))

def main():
    for X in range(parameters["min_X"], parameters["max_X"]+1):
        print("***** Experiment {} *****".format(X))
        one_X(X)

def write_readme(loc, X, Y, n_agents, n_splits, max_pr):
    data = "loc = {}; X = {}; Y = {}; n_agents = {}; n_splits = {}; max_pr = {}".format(
        loc,
        X,
        Y,
        n_agents,
        n_splits,
        max_pr
    )

    with open(loc, "w") as f:
        f.write(data)

def run_test(start_temp, agents, tasks):
    annealer = Annealer(agents, tasks, start_temp, 0.0005, parameters["time"])

    start = timeit.default_timer()
    schedule = annealer.optimize_schedule()
    print(timeit.default_timer() - start)
    return annealer.assignment_probability(schedule), timeit.default_timer() - start

if __name__ == "__main__": main()