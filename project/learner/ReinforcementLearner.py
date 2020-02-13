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
        # self.init_actor_critic()

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

            board_state = self.convert_flat_state_string(
                currentGame.get_board_state()
            )
            legal_moves = currentGame.get_legal_moves(True)

            while legal_moves:
                # Add the board state and actions if not in policy
                if(board_state not in self.actor.policy.keys()):
                    self.actor.add_sap_policy(board_state, legal_moves)
                # Add the board state if not in values
                if(board_state not in self.critic.values.keys()):
                    self.critic.add_state_value(board_state)

                # Update elegibility for the current board state
                self.critic.update_eligibilities(
                    current_state=board_state,
                    update_state=board_state
                )
                self.actor.update_eligibilities(
                    current_state=board_state,
                    update_state=board_state
                )

                # Get and make the next move
                prev_state = board_state
                prev_move = self.actor.get_move(board_state)

                # Parse move result
                result = currentGame.try_move(prev_move)
                reward, board_state, legal_moves = result
                board_state = self.convert_flat_state_string(board_state)

                # Update critic temporal difference
                temporal_diff = self.critic.calc_temp_diff(
                    reward,
                    board_state,
                    prev_state
                )
                print(temporal_diff)

    def init_actor_critic(self):
        game_structure = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"]
        )

        # TODO: Function in PegGame for returning all possible states
        all_states = game_structure.get_board_state_permutations()
        label_states = list(map(
            lambda x: self.convert_flat_state_string(x), all_states
            ))
        # TODO: Function in PegGame for returning all possible SAP

        print(label_states)

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
