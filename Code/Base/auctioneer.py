from copy import deepcopy
import random

from Base.agent import Agent
from Base.task import Task
from Base.problem_generator import generate_painter

X = 12
Y = 12

def main():
    agents, tasks = generate_painter(X, Y, 3)

    # We give back m tasks in a giveback phase, and each iteration we assign one task,
    # so for m agents we should have a giveback probability < 1/m
    auctioneer = Auctioneer(agents, tasks, 0.25)#1 / ( * len(agents)))

    schedule = auctioneer.optimize_schedule()

    Agent.print_schedule(X, Y, auctioneer, schedule)

class Auctioneer:
    def __init__(self, agents, tasks, p):
        self.agents = agents
        self.tasks = tasks
        self.p = p

    def optimize_schedule(self):
        task_list = deepcopy(self.tasks)
        random.shuffle(task_list)
        #task_list = sorted(task_list, key=lambda x: x.chosen_probability())

        while len(task_list) > 0:
            #print(len(task_list))

            assigned_tasks = sum([len(x.schedule) for x in self.agents])
            #print(assigned_tasks)
            #print("Agents have {} tasks; {} tasks left; {} in total, expecting {}".format(assigned_tasks, len(task_list), assigned_tasks + len(task_list), len(self.tasks)))
            assert assigned_tasks + len(task_list) == len(self.tasks)

            # Check for giveback phase
            r = random.random()
            if r < self.p:
                #print("Doing a giveback phase")
                for agent in self.agents:
                    agent_wt_idx = agent.worst_task_idx()
                    if agent_wt_idx >= 0:
                        task_list += [agent.schedule[agent_wt_idx]]
                        del agent.schedule[agent_wt_idx]

            cur_task = task_list.pop(0)

            best_overall_probability = -1
            best_overall_agent = None
            best_overall_agent_schedule = None

            random.shuffle(self.agents)

            #print("BEFORE", [x.parameters["name"] + ": " + str(len(x.schedule)) for x in self.agents])

            for cur_agent in self.agents:
                new_schedule = cur_agent.bid_on_task(cur_task)
                assert len(new_schedule) == len(cur_agent.schedule) + 1

                #probability_product = 1
                probability_sum = 0
                for a in self.agents:
                    if a is cur_agent:
                        agent_pr = a.schedule_success_probability(new_schedule)
                    else:
                        agent_pr = a.schedule_success_probability(a.schedule)

                    #probability_product *= agent_pr
                    probability_sum += agent_pr

                # assert probability_product >= 0 and probability_product <= 1
                #
                # if probability_product > best_overall_probability:
                #     best_overall_probability = probability_product
                #     best_overall_agent = cur_agent
                #     best_overall_agent_schedule = new_schedule

                assert probability_sum >= 0 and probability_sum <= 1

                if probability_sum > best_overall_probability:
                    best_overall_probability = probability_sum
                    best_overall_agent = cur_agent
                    best_overall_agent_schedule = new_schedule

            #print("Best agent:", best_overall_agent.parameters["name"])
            best_overall_agent.schedule = best_overall_agent_schedule

            #print([(str(x[0]), x[1]) for x in agent_probabilities.items()])

            #print("AFTER", [x.parameters["name"] + ": " + str(len(x.schedule)) for x in self.agents])

        #for a in self.agents:
        #    print(a.parameters["name"], "->", a.schedule)

        return {a: a.schedule for a in self.agents}

    def assignment_probability(self, schedule):
        # Calculate the probability that each agent fails, equal to the product of 1 - the probability that each agent succeeds        pr_all_fail = 0
        total_success = 0

        for agent in schedule:
            total_success += agent.schedule_success_probability(schedule[agent])

        return total_success

if __name__ == "__main__": main()