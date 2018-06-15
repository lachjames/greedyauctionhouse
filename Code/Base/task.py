class Task():
    def __init__(self, parameters):
        self.parameters = parameters

    def chosen_probability(self):
        return self.parameters["chosen_probability"]

    def __str__(self):
        return self.parameters["name"]