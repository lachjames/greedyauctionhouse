from optimizer import Optimizer
import random

class Greedy_Optimizer(Optimizer):
    def __init__(self, definition):
        self.definition = definition

    def schedule(self):
        agent_total_time = {a : 0 for a in self.definition.agents}
        schedule = {a: [] for a in self.definition.agents}

        # We want to optimize
        random.shuffle(self.definition.tasks)
        for task in self.definition.tasks:
            # We give each task to the agent with the lowest total workload right now
            assigned_agent = min(agent_total_time, key=lambda x: agent_total_time.get(x) + x.task_time(schedule[x], task))
            schedule[assigned_agent] += [task]
            agent_total_time[assigned_agent] += assigned_agent.task_time(schedule[assigned_agent], task)
            #print(task)

        return schedule, agent_total_time