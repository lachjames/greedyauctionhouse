import math
import random

class Agent():
    def __init__(self, parameters):
        self.schedule = []
        self.parameters = parameters

        # self.cached_times = []

    def best_pos_search(self, task, positions):
        # Our base case is when we have less than 5 tasks
        if len(positions) <= 10:
            best_position, best_schedule = self.best_pos_brute_force(task, positions)
            return best_position, best_schedule

        # Otherwise, we will split the list into five pieces, choose the middle of each
        # piece and test which position of those is best
        # Then we will recurse into that piece until we reach the base case.

        # We find a list of five positions, each 1/10, 3/10, ..., 9/10ths of the way
        # through the list
        split_positions = [positions[0] + int(len(positions) * i / 10) for i in (1, 3, 5, 7, 9)]
        #print(split_positions)
        best_position, best_schedule = self.best_pos_brute_force(task, split_positions)

        #print(best_position)

        tenth = len(positions) // 10
        # We take the segment of the list from (2 * i / 10) to (2 * (i + 1) / 10)
        best_start = max(best_position - tenth, 0)
        best_end = min(best_position + tenth, len(self.schedule))

        return self.best_pos_search(task, range(best_start, best_end + 1))

    def best_pos_brute_force(self, task, positions):
        best_schedule = None
        best_schedule_probability = -1
        best_position = -1

        for possible_position in positions:
            new_schedule = self.schedule[:possible_position] + [task] + self.schedule[possible_position:]

            assert len(new_schedule) == len(self.schedule) + 1

            p = self.schedule_success_probability(new_schedule)
            #print(p)

            if p > best_schedule_probability:
                best_schedule_probability = p
                best_schedule = new_schedule
                best_position = possible_position

        #print(best_position)

        return best_position, best_schedule

    def bid_on_task(self, task):
        # NOTE (Potentially flawed, due to very little actual data)
        # Our method tends to do worse than straight-up greedy search when we use the brute force
        # search, but it actually does better when we use the random search and have a larger number of tasks!
        # Perhaps this is a good use case, when we have imperfect information
        # We could also check whether accounting for the discrepency in computations by increasing
        # the amount of intervals straight-up greedy search uses closes the gap
        best_position, best_schedule = self.best_pos_search(task, range(len(self.schedule) + 1))
        # best_position, best_schedule = self.best_pos_brute_force(task, range(len(self.schedule) + 1))
        return best_schedule

    def worst_task_idx(self):
        # The agent returns the task whose absense yields the highest probability
        if len(self.schedule) == 0:
            return -1

        best_pr = 0
        worst_task_index = 0

        for i, task in enumerate(self.schedule):
            schedule_without_i = self.schedule[:i] + self.schedule[i+1:]
            pr = self.schedule_success_probability(schedule_without_i)
            # print(pr)
            if pr > best_pr:
                best_pr = pr
                worst_task_index = i

        #print(self.parameters["name"] + ":" + str(worst_task_index))

        return worst_task_index

    def schedule_success_probability(self, sch):
        pr_sum = 0
        cumulative_times = self.schedule_time_accumulative(sch)
        for i, task in enumerate(sch):
            task_success = self.task_success_probability(task, sch[:i], cumulative_times[i])
            if task_success < 0 or task_success > 1:
                print("Task success probability {} found, which is not possible!".format(task_success))
                exit()
            pr_sum += task_success * task.chosen_probability()

        if pr_sum < 0 or pr_sum > 1:
            print("Schedule success probability {} found, which is not possible!".format(pr_sum))
            exit()

        return pr_sum
    #
    # def insert_update_cached_times(self, item, pos):
    #     item_time = self.parameters["task_time"]
    #     if pos > 0:
    #         # Calculate
    #         new_prev_time = self.travel_time(self.schedule[pos - 1], item)
    #     else:
    #         new_prev_time = 0
    #
    #     if pos < len(self.schedule):
    #         # calculate time to next
    #         new_next_time = self.travel_time(item, self.schedule[pos])
    #     else:
    #         new_next_time = 0
    #
    #     if pos > 0 and pos < len(self.schedule):
    #         # Calculate old travel time
    #         old_travel_time = self.travel_time(self.schedule[pos - 1], self.schedule[pos])
    #     else:
    #         old_travel_time = 0
    #
    #     self.cached_items.insert(item_time + new_prev_time, pos)
    #     for i in range(pos, len(self.schedule)):
    #         self.cached_times[i] += item_time + new_prev_time + new_next_time - old_travel_time
    #
    # def remove_update_cached_times(self, pos):
    #     # We need to remove the time taken to do the item, and add back the time to jump from pos-1 to pos+1
    #     item_time = self.parameters["task_time"]
    #     if pos > 0:
    #         # Calculate
    #         old_prev_time = self.travel_time(self.schedule[pos - 1], self.schedule[pos])
    #     else:
    #         old_prev_time = 0
    #
    #     if pos < len(self.schedule):
    #         # calculate time to next
    #         old_next_time = self.travel_time(self.schedule[, self.schedule[pos])
    #     else:
    #         old_next_time = 0
    #
    #     if pos > 0 and pos < len(self.schedule) - 1:
    #         # Calculate old travel time
    #         new_travel_time = self.travel_time(self.schedule[pos - 1], self.schedule[pos + 1])
    #     else:
    #         new_travel_time = 0
    #
    #     self.cached_items.insert(item_time + new_prev_time, pos)
    #     for i in range(pos, len(self.schedule)):
    #         self.cached_times[i] -= item_time + new_prev_time + new_next_time - old_travel_time
    #         self.cached_times[i] += new_travel_time
    #
    # def travel_time(self, taskA, taskB):
    #     x = abs(taskA.parameters["i"] - taskB.parameters["i"])
    #     y = abs(taskA.parameters["j"] - taskB.parameters["j"])
    #     dist = (x ** 2 + y ** 2) ** 0.5
    #     return dist / self.parameters["move_speed"]
    #
    # def add_task_to_schedule(self, task, pos):
    #     self.update_schedule_time_accumulative(task, pos)
    #     self.schedule.insert(task, pos)
    #
    # def remove_task_from_schedule(self, pos):
    #     self.remove_schedule_time_accumulative(task, pos)
    #     del self.schedule[pos]

    def schedule_time_accumulative(self, schedule):
        if schedule is None:
            return []

        time_taken = 0
        times = []
        for i, task in enumerate(schedule):
            time_taken += self.parameters["task_time"]
            if i != 0:
                x = abs(schedule[i-1].parameters["i"] - task.parameters["i"])
                y = abs(schedule[i-1].parameters["j"] - task.parameters["j"])
                dist = (x ** 2 + y ** 2) ** 0.5
                time_taken += dist / self.parameters["move_speed"]
            times += [time_taken]

        return times

    # def schedule_time(self, schedule):
    #     time_taken = 0
    #
    #     for i, task in enumerate(schedule):
    #         if i != 0:
    #             x = abs(schedule[i-1].parameters["i"] - task.parameters["i"])
    #             y = abs(schedule[i-1].parameters["j"] - task.parameters["j"])
    #             dist = (x ** 2 + y ** 2) ** 0.5
    #             time_taken += dist / self.parameters["move_speed"]
    #     return time_taken

    def task_success_probability(self, task, prev_schedule, prev_time_taken):
        # This is customised to each situation
        pr = self.parameters["skill"] * self.time_multiplier(prev_time_taken)
        return pr

    def time_multiplier(self, t):
        return 1 / (math.e ** (t / 100))

    def __str__(self):
        return self.parameters["name"]

    @staticmethod
    def print_schedule(X, Y, optimizer, schedule):
        for agent in schedule:
            agent_schedule = schedule[agent]
            cumulative_time = agent.schedule_time_accumulative(agent_schedule)
            agent_time = cumulative_time[-1] if len(cumulative_time) > 0 else 0
            print("{} takes {} time".format(agent.parameters["name"], agent_time))
            for task in schedule[agent]:
                print("  - {}".format(task.parameters["name"]))

        task_agent = {}
        for agent in schedule:
            for task in schedule[agent]:
                task_ij = (task.parameters["i"], task.parameters["j"])
                task_agent[task_ij] = agent

        # class bcolors:
        #     HEADER = '\033[95m'
        #     OKBLUE = '\033[94m'
        #     OKGREEN = '\033[92m'
        #     WARNING = '\033[93m'
        #     FAIL = '\033[91m'
        #     ENDC = '\033[0m'
        #     BOLD = '\033[1m'
        #     UNDERLINE = '\033[4m'
        cols = [
            '\033[95m',
            '\033[94m',
            '\033[92m',
            '\033[93m',
            '\033[91m',
            '\033[0m',
            '\033[1m',
            '\033[4m',
        ]
        for i in range(X):
            for j in range(Y):
                try:
                    agent_num = int(task_agent[(i, j)].parameters["name"])
                except:
                    continue
                print(cols[agent_num], end="")
                print(agent_num, end=" ")
            print()

        print("Total probability of success = {}".format(optimizer.assignment_probability(schedule)))

    def __str__(self):
        return str(self.parameters) + "\n" + str(self.schedule) + "\n"
