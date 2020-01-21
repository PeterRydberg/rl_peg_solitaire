from Actor import Actor
from Critic import Critic


class ReinforcementLearner:
    def __init__(self):
        self.critic = Critic()
        self.actor = Actor()
