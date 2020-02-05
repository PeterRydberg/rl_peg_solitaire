from .Actor import Actor
from .Critic import Critic
from game.PegGame import PegGame


class ReinforcementLearner:
    def __init__(
        self,
        episodes,
        game_settings,
        critic_settings,
        actor_settings
    ):
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
        self.critic.initialize_critic()
        self.actor.initialize_actor()

        # Iterate through all episodes
        for episode in range(self.episodes):

            # Initializes new game using game settings
            currentGame = PegGame(
                self.game_settings["board_type"],
                self.game_settings["board_size"],
                self.game_settings["initial_empty"],
                self.game_settings["live_update_frequency"],
                (episode + 1) in self.game_settings["display_game"],
                episode + 1
            )

            initial_board_state = currentGame.get_board_state()
            initial_legal_moves = currentGame.get_legal_moves()
            self.critic.update_eligibilities(
                                            initial_board_state,
                                            initial_legal_moves
                                            )

            # currentGame.try_move((3, 3), 4)
