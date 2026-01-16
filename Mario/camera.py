class Camera:
    def __init__(self):
        self.offset_x = 0

    def follow(self, target):
        self.offset_x = target.rect.centerx - 400
        self.offset_x = max(0, self.offset_x)
