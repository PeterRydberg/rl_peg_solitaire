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

            # Initial elegibility update for the current board state
            self.critic.update_eligibilities(
                state=board_state,
                decay=False
            )
            for action in legal_moves:
                self.actor.update_eligibilities(
                    state=board_state,
                    action=action,
                    decay=False
                )

            while legal_moves:
                # Add the board state and actions if not in policy
                if(board_state not in self.actor.policy.keys()):
                    self.actor.add_sap_policy(board_state, legal_moves)
                # Add the board state if not in values
                if(board_state not in self.critic.values.keys()):
                    self.critic.add_state_value(board_state)

                # Get and make the next move
                prev_state = board_state
                prev_action = self.actor.get_move(board_state)
                result = currentGame.try_move(prev_action)

                # Parse move result
                reward, board_state, legal_moves = result
                board_state = self.convert_flat_state_string(board_state)

                # Update critic temporal difference
                temporal_diff = self.critic.calc_temp_diff(
                    reward,
                    board_state,
                    prev_state
                )

                # Update elegibility for the board state used
                self.critic.update_eligibilities(
                    state=prev_state,
                    decay=False
                )
                self.actor.update_eligibilities(
                    state=prev_state,
                    action=prev_action,
                    decay=False
                )

                # Updates critic values, actor policy and elegibilities
                self.value_policy_update(
                    prev_state,
                    prev_action,
                    temporal_diff
                )

    def value_policy_update(self, prev_state, prev_action, temporal_diff):
        # Update critic values and critic eligibility
        self.critic.update_state_value(prev_state, temporal_diff)
        self.critic.update_eligibilities(prev_state, True)

        # Update critic values and critic eligibility
        self.actor.update_sap_policy(prev_state, prev_action, temporal_diff)
        self.actor.update_eligibilities(prev_state, prev_action, True)

    # Converts the Peghole object state to bitstring (label)
    def convert_flat_state_string(self, board_state):
        state_string = ""
        for peghole in list(itertools.chain(*board_state)):
            if(peghole.content == "filled"):
                state_string += "1"
            elif(peghole.content == "empty"):
                state_string += "0"

        return state_string
