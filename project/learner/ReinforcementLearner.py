from .Actor import Actor
from .Critic import Critic
from game.PegGame import PegGame

import itertools


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
        self.init_actor_critic()

        # Iterate through all episodes
        for episode in range(self.episodes):

            # Reset all eligibilities before episode
            self.critic.reset_elegibilities()
            self.actor.reset_elegibilities()

            # Initializes new game using game settings
            currentGame = PegGame(
                self.game_settings["board_type"],
                self.game_settings["board_size"],
                self.game_settings["initial_empty"],
                self.game_settings["live_update_frequency"],
                (episode + 1) in self.game_settings["display_game"],
                f'Episode {episode + 1}'
            )

            initial_board_state = self.convert_flat_state_string(
                    currentGame.get_board_state()
                )
            initial_legal_moves = currentGame.get_legal_moves()

            self.critic.update_eligibilities(
                current_state=initial_board_state,
                update_state=initial_board_state
            )
            self.actor.update_eligibilities(
                current_state=initial_board_state,
                update_state=initial_board_state
            )

    def init_actor_critic(self):
        game_structure = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"]
        )

        # TODO: Function in PegGame for returning all possible states
        # TODO: Function in PegGame for returning all possible SAP

        self.critic.initialize_critic()
        self.actor.initialize_actor()

    # Converts the Peghole object state to bitstring (label)
    def convert_flat_state_string(self, board_state):
        state_string = ""
        for peghole in list(itertools.chain(*board_state)):
            if(peghole.content == "filled"):
                state_string += "1"
            elif(peghole.content == "empty"):
                state_string += "0"

        return state_string
