from unittest import TestCase

from Base.task import Task

class TestTask(TestCase):
    def test_chosen_probability(self):
        t = Task(parameters={
            "chosen_probability": 0.01,
            "name": "Test"
        })
        x = t.chosen_probability()
        assert x == 0.01, "Chosen probability should be {} but is {}".format(0.01, x)