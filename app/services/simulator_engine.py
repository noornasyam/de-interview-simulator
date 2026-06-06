class SimulatorEngine:

    def __init__(self, platform, level, mode):
        self.platform = platform
        self.level = level
        self.mode = mode
        self.history = []

    def generate_question(self):
        pass

    def evaluate_answer(self, question, answer):
        pass

    def generate_follow_up(self, question, answer, feedback):
        pass

    def generate_final_report(self):
        pass