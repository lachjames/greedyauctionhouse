from copy import deepcopy
import random, math, timeit

#from matplotlib import pyplot as plt

from Base.agent import Agent
from Base.task import Task
from Base.problem_generator import generate_painter

from Base.auctioneer import Auctioneer

X = 12
Y = 12

def main():
    agents, tasks = generate_painter(X, Y, 3)

    # nFeas = The number of feasible 1-moves
    # Given a schedule, we can move tasks equal to the number of agents.
    # Using the result by Osman, we set alpha = n * Nfeas, gamma = n
    alpha = math.factorial(X * Y)
    # The number of iterations is n

    annealer = Annealer(agents, tasks, 0.1, 0.0001, 120)

    schedule = annealer.optimize_schedule()

    Agent.print_schedule(X, Y, annealer, schedule)

class Annealer:
    # Similar to techniques discussed in:
    # Heuristics for the generalised assignment problem: simulated annealing and tabu search approaches -- IH Osman

    def __init__(self, agents, tasks, init_temp, final_temp, max_time):
        self.agents = agents
        self.tasks = tasks
        self.init_temp = init_temp
        self.final_temp = final_temp
        self.max_time = max_time

    def optimize_schedule(self):
        temp = self.init_temp

        self.random_schedule()
        #self.greedy_schedule()

        k = 0
        x = []

        t_reset = self.init_temp

        cur_pr = self.assignment_probability(self.make_schedule())

        start = timeit.default_timer()

        best_schedule = None
        best_schedule_pr = -1
        best_schedule_temp = -1

        while temp > self.final_temp:
            # Check if we have reached a new maximum
            #print(cur_pr)
            if cur_pr > best_schedule_pr:
                #print("New max pr={}".format(cur_pr))
                best_schedule = self.make_schedule()
                best_schedule_pr = cur_pr
                best_schedule_temp = temp

            if k % 10 == 0:
                if (timeit.default_timer() - start) > self.max_time:
                    break
                print(k, temp, cur_pr)
            x += [cur_pr]
            temp = self.temp_decrement(temp, k)
            k += 1

            #print(temp)
            #print(cur_pr)
            #if temp < 75:
            #    print(temp)
            #    t_reset = self.temp_increment(temp, t_reset, temp + 0.001, k)
            #    temp = t_reset

            # Generate a 1-move
            fa, fp, ta, tp = self.random_move()

            # Make the move
            self.make_move(fa, fp, ta, tp)

            # Check if the move is better or, if not, how much worse it is
            new_pr = self.cur_assignment_probability()

            if new_pr < cur_pr:
                # We will reverse the move, unless the condition is met
                delta = new_pr - cur_pr
                b = 1 / math.exp(- delta / temp)
                r = random.random()
                #print(b)
                if r < b:
                    # Reverse the move if the condition is not met
                    self.make_move(ta, tp, fa, fp)

            cur_pr = new_pr

        #print(x)
        #plt.plot(range(len(x)), x)
        #plt.show()

        # Set the current schedule to the best schedule we found
        for i in range(len(self.agents)):
            self.agents[i].schedule = best_schedule[self.agents[i]]

        #print("Best probability: {}".format(best_schedule_pr))
        return best_schedule

    def make_schedule(self):
        return {a: a.schedule[:] for a in self.agents}

    def temp_decrement(self, t, k):
        # Decrement rule from Osman
        # Moving one task at a time, to any agent who doesn't have it, we find
        # nFeas = numTasks * (numAgents - 1)
        nFeas = len(self.tasks) * (len(self.agents) -  1)

        # We use Osman's values for alpha and gamma:
        alpha = len(self.tasks) * nFeas
        gamma = len(self.tasks)

        # We calculate beta_k using Osman's rule
        b_k_numerator = self.init_temp - self.final_temp
        b_k_denominator = (alpha + gamma * math.sqrt(k)) * self.init_temp * self.final_temp

        b_k = b_k_numerator / b_k_denominator

        return t / (1 + b_k * t)

    # def temp_increment(self, t, t_reset, best_t, k):
    #     t_reset =  max(t_reset / 2, best_t)
    #     return t_reset

    def random_move(self):
        # Create a random 1-move by transferring a task from one agent to another agent
        from_agent = random.randint(0, len(self.agents) - 1)
        while len(self.agents[from_agent].schedule) == 0:
            from_agent = random.randint(0, len(self.agents) - 1)

        from_position = random.randint(0, len(self.agents[from_agent].schedule) - 1)

        # We don't want to assign the same task to the same agent
        to_agent = from_agent
        while to_agent == from_agent:
            to_agent = random.randint(0, len(self.agents) - 1)

        to_position = random.randint(0, len(self.agents[to_agent].schedule))

        return from_agent, from_position, to_agent, to_position

    def make_move(self, from_agent, from_position, to_agent, to_position):
        t = self.agents[from_agent].schedule.pop(from_position)
        self.agents[to_agent].schedule.insert(to_position, t)

    def random_schedule(self):
        random.shuffle(self.tasks)
        agent_list = self.agents * len(self.tasks)

        schedule = {a: [] for a in self.agents}
        for t in self.tasks:
            schedule[agent_list.pop(0)] += [t]

        for agent in self.agents:
            agent.schedule = schedule[agent]

    def greedy_schedule(self):
        auc = Auctioneer(self.agents, self.tasks, 0.1)
        sch = auc.optimize_schedule()
        for agent in self.agents:
            agent.sch = sch[agent]

    def cur_assignment_probability(self):
        return self.assignment_probability(self.make_schedule())

    def assignment_probability(self, schedule):
        # Calculate the probability that each agent fails, equal to the product of 1 - the probability that each agent succeeds        pr_all_fail = 0
        total_success = 0

        for agent in schedule:
            total_success += agent.schedule_success_probability(schedule[agent])

        return total_success

if __name__ == "__main__": main()