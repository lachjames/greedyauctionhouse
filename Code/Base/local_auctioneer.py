from copy import deepcopy
import random

from Base.agent import Agent
from Base.task import Task
from Base.problem_generator import generate_painter
from Base.auctioneer import Auctioneer

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

#X = 12
#Y = 12

def main():
    for x in range(12, 15):
        agents, tasks = generate_painter(x, x, 3)
        for p in [0, 0.05, 0.1, 0.15, 0.2]:
            results = []
            for n in range(10):
                # We give back m tasks in a giveback phase, and each iteration we assign one task,
                # so for m agents we should have a giveback probability < 1/m
                auctioneer = Local_Auctioneer(deepcopy(agents), deepcopy(tasks), p)#1 / ( * len(agents)))
                local_schedule = auctioneer.optimize_schedule()
                local_pr = auctioneer.assignment_probability(local_schedule)

                global_auctioneer = Auctioneer(deepcopy(agents), deepcopy(tasks), p)
                global_schedule = global_auctioneer.optimize_schedule()
                global_pr = auctioneer.assignment_probability(global_schedule)

                #print(",".join([str(x) for x in (x, p, local_pr, global_pr)]))
                results += [(local_pr, global_pr)]

            local_results, global_results = zip(*results)

            local_mean = np.mean(local_results)
            global_mean = np.mean(global_results)

            # https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
            local_min_ci, local_max_ci = st.t.interval(0.95, len(local_results) - 1, loc=np.mean(local_results), scale=st.sem(local_results))
            global_min_ci, global_max_ci = st.t.interval(0.95, len(global_results) - 1, loc=np.mean(global_results), scale=st.sem(global_results))

            A = [x, p, local_mean, global_mean, local_min_ci, local_max_ci, global_min_ci, global_max_ci]

            print(",".join([str(z) for z in A]))

class Local_Auctioneer:
    def __init__(self, agents, tasks, p):
        self.agents = agents
        self.tasks = tasks
        self.p = p

    def optimize_schedule(self):
        schedules = {}
        for a in self.agents:
            auc = Auctioneer([a], deepcopy(self.tasks), self.p)
            schedules[a] = auc.optimize_schedule()
        return {agent : agent.schedule for agent in schedules}

    def assignment_probability(self, schedule):
        # Calculate the probability that each agent fails, equal to the product of 1 - the probability that each agent succeeds        pr_all_fail = 0
        total_success = 1

        for agent in schedule:
            total_success *= (1 - agent.schedule_success_probability(schedule[agent]))

        return 1 - total_success

if __name__ == "__main__": main()