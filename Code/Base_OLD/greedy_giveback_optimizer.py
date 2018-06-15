from optimizer import Optimizer
import random

from copy import deepcopy

class Greedy_Giveback_Optimizer(Optimizer):
    def __init__(self, agents, tasks, pr_giveback):
        self.agents = agents
        self.tasks = tasks
        self.pr_giveback = pr_giveback

    def schedule(self):
        agent_total_time = {a : 0 for a in self.agents}
        schedule = {a: [] for a in self.agents}

        tasks = deepcopy(self.tasks)

        # We want to optimize
        random.shuffle(tasks)
        for task in tasks:
            if random.random() < self.pr_giveback:
                # Each agent puts one task back into the task pool
                for agent in self.agents:
                    # Each agent gives back a task
                    giveback_task = agent.most_inconvenient(schedule[agent])
                    if giveback_task != None:
                        tasks.append(giveback_task)
                        schedule[agent].remove(giveback_task)
            # We give each task to the agent with the lowest total workload right now
            assigned_agent = min(agent_total_time, key=lambda x: agent_total_time.get(x) + x.task_time(schedule[x], task))
            schedule[assigned_agent] += [task]
            agent_total_time[assigned_agent] += assigned_agent.task_time(schedule[assigned_agent], task)
            #print(task)

        return schedule, agent_total_time