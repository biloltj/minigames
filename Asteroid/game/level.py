class LevelManager:
    def __init__(self):
        self.level = 1

    def next(self):
        self.level += 1

    def speed(self):
        return 1 + self.level * 0.25

    def boss_level(self):
        return self.level % 5 == 0
