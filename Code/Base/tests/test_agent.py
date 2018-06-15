from unittest import TestCase

from Base.agent import Agent
from Base.task import Task

tX = Task(parameters={
    "chosen_probability": 0.2,
    "name": "Test",
    "i": 1,
    "j": 1
})

t1 = Task(parameters={
    "chosen_probability": 0.003,
    "name": "Test",
    "i": 1,
    "j": 1
})

t2 = Task(parameters={
    "chosen_probability": 0.001,
    "name": "Test",
    "i": 1,
    "j": 2
})

t3 = Task(parameters={
    "chosen_probability": 0.001,
    "name": "Test",
    "i": 3,
    "j": 4
})

tI = Task(parameters={
    "chosen_probability": 0.1,
    "name": "Test",
    "i": 0,
    "j": 0
})

tJ = Task(parameters={
    "chosen_probability": 0,
    "name": "Test",
    "i": 3,
    "j": 3
})

tK = Task(parameters={
    "chosen_probability": 0.002,
    "name": "Test",
    "i": 1,
    "j": 2
})

class TestAgent(TestCase):
    def test_best_pos_search_base_case(self):
        schedules = [
            [],
            [tX],
            [t1, t2, t3]
        ]

        expectations = [
            (0, 0, 0),
            (1, 1, 1),
            (0, 3, 1)
        ]

        for i, schedule in enumerate(schedules):
            a = Agent(parameters={
                "name": "1",
                "skill": 0.95,
                "task_time": 1,
                "move_speed": 1
            })

            a.schedule = schedule

            p_i = a.best_pos_search(tI, range(len(a.schedule) + 1))
            p_j = a.best_pos_search(tJ, range(len(a.schedule) + 1))
            p_k = a.best_pos_search(tK, range(len(a.schedule) + 1))

            p_ijk = p_i[0], p_j[0], p_k[0]
            assert p_ijk == expectations[i], "Expected {} but got {}".format(expectations[i], p_ijk)

    def test_best_pos_search_recursion(self):
        schedules = [
            [t1] * 100 + [t2] * 100 + [t3] * 100
        ]

        expectations = [
            (0, 300, 120) # 120 seems to be the result returned by the code and appears to be correct, but I'm not convinced...
        ]

        for i, schedule in enumerate(schedules):
            a = Agent(parameters={
                "name": "1",
                "skill": 0.95,
                "task_time": 1,
                "move_speed": 1
            })

            a.schedule = schedule

            p_i = a.best_pos_search(tI, range(len(a.schedule) + 1))
            p_j = a.best_pos_search(tJ, range(len(a.schedule) + 1))
            p_k = a.best_pos_search(tK, range(len(a.schedule) + 1))

            p_ijk = p_i[0], p_j[0], p_k[0]
            #print(p_ijk)
            assert p_ijk == expectations[i], "Expected {} but got {}".format(expectations[i], p_ijk)

    def test_best_pos_brute_force(self):
        self.fail()

    def test_bid_on_task(self):
        self.fail()

    def test_worst_task_idx(self):
        a = Agent(parameters={
            "name": "1",
            "skill": 0.95,
            "task_time": 1,
            "move_speed": 1
        })

        a.schedule = [t1] * 10 + [tJ] + [t1] * 10

        wt = a.worst_task_idx()

        assert wt == 10, "Should have been {} but was {}".format(10, wt)

    def test_schedule_success_probability(self):
        self.fail()

    def test_schedule_time_accumulative(self):
        self.fail()

    def test_task_success_probability(self):
        self.fail()

    def test_time_multiplier(self):
        self.fail()

    def test_print_schedule(self):
        self.fail()
