from Actor import Actor
from Critic import Critic


class ReinforcementLearner:
    def __init__(self, episodes, game_settings, critic_settings, actor_settings):
        self.episodes = episodes
        self.game_settings = game_settings

        self.critic = Critic(
                            critic_settings["c_type"],
                            critic_settings["c_learning_rate"],
                            critic_settings["c_eligibility_decay"],
                            critic_settings["c_discount_factor"],
                            critic_settings["c_nn_layers"]
                            )
        self.actor = Actor(
                            actor_settings["a_learning_rate"],
                            actor_settings["a_eligibility_decay"],
                            actor_settings["a_discount_factor"],
                            actor_settings["a_e_greediness"]
                            )


    def train_model(self):
        pass
