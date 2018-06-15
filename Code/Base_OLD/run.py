import math

from task import Task
from agent import Agent
#from greedy_optimizer import Greedy_Optimizer
from greedy_giveback_optimizer import Greedy_Giveback_Optimizer

agents = [
    Agent("Agent 1", 0.9, 4),
    Agent("Agent 2", 0.8, 3),
    Agent("Agent 3", 0.6, 1),
    Agent("Agent 4", 0.2, 0.5)
]

tasks = []
sum = 0

X = 10
Y = 50

for i in range(X):
    for j in range(Y):
        p = 5 - abs(i - 5) + 5 - abs(j - 5)
        sum += p
        t = Task("Task_{}_{}".format(i, j), p, {"i": i, "j": j})
        tasks += [t]

for task in tasks:
    task.p_chosen /= sum

optimizer = Greedy_Giveback_Optimizer(agents, tasks, 0.1)

schedule, total_time = optimizer.schedule()

for agent in schedule:
    print("{} takes {} time".format(agent.name, total_time[agent]))
    for task in schedule[agent]:
        print("  - {}".format(task.name))
task_agent = {}
for agent in schedule:
    for task in schedule[agent]:
        task_ij = (task.parameters["i"], task.parameters["j"])
        task_agent[task_ij] = agent

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for i in range(X):
    for j in range(Y):
        agent_num = int(task_agent[(i, j)].name.replace("Agent ", ""))
        if agent_num == 1:
            print(bcolors.HEADER, end="")
        elif agent_num == 2:
            print(bcolors.OKBLUE, end="")
        elif agent_num == 3:
            print(bcolors.OKGREEN, end="")
        elif agent_num == 4:
            print(bcolors.FAIL, end="")
        print(agent_num, end=" ")
    print()