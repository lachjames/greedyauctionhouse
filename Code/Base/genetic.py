from copy import deepcopy
import random, math, timeit

#from matplotlib import pyplot as plt

from Base.agent import Agent
from Base.task import Task
from Base.problem_generator import generate_painter

import numpy as np

import multiprocessing as mp

NUM_PROCESSES = mp.cpu_count() - 1
print("{} PROCESSES RUNNING".format(NUM_PROCESSES))

X = 12
Y = 12

def main():
    agents, tasks = generate_painter(X, Y, 3)

    # nFeas = The number of feasible 1-moves
    # Given a schedule, we can move tasks equal to the number of agents.
    # Using the result by Osman, we set alpha = n * Nfeas, gamma = n
    alpha = math.factorial(X * Y)
    # The number of iterations is n

    annealer = Annealer(agents, tasks, 2500, 100, 0.1, 1)

    schedule = annealer.optimize_schedule()

    Agent.print_schedule(X, Y, annealer, schedule)

class Annealer:
    # Similar to techniques discussed in:
    # Heuristics for the generalised assignment problem: simulated annealing and tabu search approaches -- IH Osman

    def __init__(self, agents, tasks, n_iter, generation_size, mutation_pr, alpha):
        self.agents = agents
        self.tasks = tasks
        self.n_iter = n_iter
        self.generation_size = generation_size
        self.mutation_pr = mutation_pr
        self.alpha = alpha

    def one_generation(self, generation, probabilities):
        # Creates a new generation of schedules, based on generation, and returns it
        #print(generation[0])

        # Crossover
        generation = self.crossover_generation(generation, probabilities)

        # Mutation
        generation = self.mutate_generation(generation)

        # Recalculate probabilities
        probabilities = self.generation_probabilities(generation)

        return generation, probabilities

    def generation_probabilities(self, generation):
        pool = mp.Pool(processes=NUM_PROCESSES)

        probabilities = pool.map(
            self.assignment_probability,
            generation
        )

        pool.close()

        probabilities = np.asarray(probabilities)

        probabilities -= np.min(probabilities)
        probabilities /= np.sum(probabilities)

        return probabilities

    def crossover_generation(self, generation, probabilities):
        # Calculate success probability of each schedule in the generation
        #probabilities = []
        #for schedule in generation:
        #    probabilities += [self.assignment_probability(schedule)]

        new_generation = []
        for _ in range(int(len(generation) * self.alpha)):
            # Pick two parents, A and B
            A = np.random.choice(generation, p=probabilities)
            B = np.random.choice(generation, p=probabilities)

            new_generation += [self.crossover_one(A, B)]

        while len(new_generation) < len(generation):
            # Add some new candidates to the population
            new_generation += [self.random_schedule()]

        return new_generation

    def crossover_one(self, A, B):
        # Performs crossover between schedules A and B.
        # For each task, we assign to schedule A's agent for the task with pr=0.5,
        # and schedule B's agent for the task with pr=0.5

        new_schedule = {x: [] for x in self.agents}
        for task in self.tasks:
            r = random.random()
            if r < 0.5:
                # Assign task as in schedule A
                agent, pos = self.find_position(task, A)
            else:
                # Assign task as in schedule B
                agent, pos = self.find_position(task, B)

            new_schedule[agent].insert(pos, task)

        return new_schedule

    def find_position(self, task, schedule):
        # Returns the agent and the index within that agent's schedule of the task

        for agent in schedule:
            if task in schedule[agent]:
                return agent, schedule[agent].index(task)

        return None, None

    def mutate_generation(self, generation):
        mutated_generation = []

        for i, schedule in enumerate(generation):
            r = random.random()
            if r < self.mutation_pr:
                mutated_generation += [self.mutate_schedule(schedule)]
            else:
                mutated_generation += [schedule]

        return mutated_generation

    def random_schedule(self):
        random.shuffle(self.tasks)
        agent_list = self.agents * len(self.tasks)

        schedule = {a: [] for a in self.agents}
        for t in self.tasks:
            schedule[agent_list.pop(0)] += [t]

        return schedule

    def best_schedule(self, generation, probabilities):
        best_idx = np.argmax(probabilities)
        return generation[best_idx]

    def optimize_schedule(self):
        generation = [ self.random_schedule() for _ in range(self.generation_size) ]
        probabilities = self.generation_probabilities(generation)

        best_overall_schedule = None
        best_overall_schedule_probability = -1

        for i in range(self.n_iter):
            generation, probabilities = self.one_generation(generation, probabilities)

            best_sch = self.best_schedule(generation, probabilities)
            best_sch_pr = self.assignment_probability(best_sch)

            print(i, ":", best_sch_pr, end="")

            if best_sch_pr > best_overall_schedule_probability:
                best_overall_schedule_probability = best_sch_pr
                best_overall_schedule = best_sch
                print(" ** NEW BEST **", end="")

            #Agent.print_schedule(X, Y, self, best_sch)
            print()

        return best_overall_schedule

    def make_schedule(self):
        return {a: a.schedule[:] for a in self.agents}

    def mutate_schedule(self, schedule):
        # Create a random 1-move by transferring a task from one agent to another agent
        from_agent = self.agents[random.randint(0, len(self.agents) - 1)]
        while len(schedule[from_agent]) == 0:
            from_agent = random.randint(0, len(self.agents) - 1)

        from_position = random.randint(0, len(schedule[from_agent]) - 1)

        # We don't want to assign the same task to the same agent
        to_agent = from_agent
        while to_agent == from_agent:
            to_agent = self.agents[random.randint(0, len(self.agents) - 1)]

        to_position = random.randint(0, len(schedule[to_agent]))

        t = schedule[from_agent].pop(from_position)
        schedule[to_agent].insert(to_position, t)

        return schedule

    def cur_assignment_probability(self):
        return self.assignment_probability(self.make_schedule())

    def assignment_probability(self, schedule):
        # Calculate the probability that each agent fails, equal to the product of 1 - the probability that each agent succeeds        pr_all_fail = 0
        total_success = 0

        for agent in schedule:
            total_success += agent.schedule_success_probability(schedule[agent])

        return total_success

if __name__ == "__main__": main()