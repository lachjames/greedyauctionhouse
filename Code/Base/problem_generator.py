from Base.agent import Agent
from Base.task import Task

def generate_painter(X, Y, num_agents):
    agents = []
    skill_diff = 1.0 / (num_agents + 1)
    time_diff = 1.0 / (2 * num_agents + 1)
    for i in range(num_agents):
        agents += [
            Agent(parameters = {
                "name": str(i),
                "skill": 1.0 - (i * skill_diff),
                "task_time": 1.0 - (i * time_diff),
                "move_speed": (i + 1)
            })
        ]
        #print(agents[-1])
    total = 0
    tasks = []

    half_diagonal = ((X**2 + Y**2) ** 0.5) / 2
    for i in range(X):
        for j in range(Y):
            # p = (X^2 + Y^2) / 4 - euclidean distance from center to (i, j)
            # = ( (i - (X/2))^2 + (j - (X/2)^2) ^ 0.5
            center_distance = ((i - X/2) ** 2 + (j - Y/2) ** 2) ** 0.5
            p = half_diagonal - center_distance
            total += p
            t = Task(parameters={
                "name": "({},{})".format(i, j),
                "i": i,
                "j": j,
                "chosen_probability": p
            })
            tasks += [t]

    for task in tasks:
        task.parameters["chosen_probability"] /= total

    #for i in range(X):
    #    for j in range(Y):
    #        print(round(tasks[i * Y + j].chosen_probability(), 2), end=" ")
    #    print("\n")

    return agents, tasks

# print(generate_painter(5, 5, 3))