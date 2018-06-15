class Task:
    def __init__(self, name, p_chosen, parameters):
        self.name = name
        self.p_chosen = p_chosen
        self.parameters = parameters

    def __str__(self):
        return str(self.name)