class Peghole:
    def __init__(self, content='empty', coordinates=(0, 0)):
        self.content = content
        self.coordinates = coordinates
        self.neighbors = []
