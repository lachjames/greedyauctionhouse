class Agent:
    def __init__(self, name, skill, time):
        self.name = name
        self.skill = skill
        self.time = time

    def task_probability(self, task):
        # Returns the probability that this agent can complete the task successfully
        return self.skill

    def task_time(self, cur_schedule, task):
        if len(cur_schedule) == 0:
            return self.time
        x = abs(cur_schedule[-1].parameters["i"] - task.parameters["i"])
        y = abs(cur_schedule[-1].parameters["j"] - task.parameters["j"])
        dist = (x ** 2 + y ** 2) ** 0.5
        return dist + self.time

    def most_inconvenient(self, cur_schedule):
        # Determines the most inconvenient task in a given schedule
        # - That is, the task that takes the most time given the previous tasks
        worst_task = None
        worst_task_time = float("-Inf")

        for i in range(len(cur_schedule)):
            schedule_up_to_i = cur_schedule[:i]
            i_time = self.task_time(schedule_up_to_i, cur_schedule[i])
            if i_time > worst_task_time:
                worst_task = cur_schedule[i]
                worst_task_time = i_time

        return worst_task

    def __str__(self):
        return str(self.name)