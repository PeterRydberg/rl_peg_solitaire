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
                            actor_settings["a_e_greediness"],
                            episodes
                            )

    def train_model(self):
        # Iterate through all episodes
        for episode in range(self.episodes):
            currentGame, board_state, legal_moves = self.init_game(episode)
            self.init_eligibilities(board_state, legal_moves)
            actions_taken = []

            while legal_moves:
                # Add the board state and actions if not in policy
                if(board_state not in self.actor.policy.keys()):
                    for action in legal_moves:
                        self.actor.add_sap_policy(board_state, action)
                # Add the board state if not in values
                if(board_state not in self.critic.values.keys()):
                    self.critic.add_state_value(board_state)

                # Get and make the next move
                prev_state = board_state
                prev_action = self.actor.get_move(board_state)
                result = currentGame.try_move(prev_action, return_reward=True)

                # Parse move result
                reward, board_state, legal_moves = result
                board_state = self.convert_flat_state_string(board_state)

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

                # Update critic temporal difference
                temporal_diff = self.critic.calc_temp_diff(
                    reward,
                    board_state,
                    prev_state
                )

                actions_taken.append((prev_state, prev_action))

                # Updates critic values, actor policy and elegibilities
                # for each state action pair
                self.value_policy_update(
                    actions_taken,
                    temporal_diff
                )
            self.actor.increase_greediness(self.episodes)

    def value_policy_update(self, actions, temporal_diff):
        for state, action in actions:
            # Update critic values and critic eligibility
            self.critic.update_state_value(state, temporal_diff)
            self.critic.update_eligibilities(state, True)

            # Update critic values and critic eligibility
            self.actor.update_sap_policy(state, action, temporal_diff)
            self.actor.update_eligibilities(state, action, True)

    # Converts the Peghole object state to bitstring (label)
    def convert_flat_state_string(self, board_state):
        state_string = ""
        for peghole in list(itertools.chain(*board_state)):
            if(peghole.content == "filled"):
                state_string += "1"
            elif(peghole.content == "empty"):
                state_string += "0"

        return state_string

    def init_game(self, episode):
        # Initializes new game using game settings
        currentGame = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"],
            self.game_settings["live_update_frequency"],
            (episode + 1) in self.game_settings["display_game"],
            f'Episode {episode + 1}'
        )

        # Gets initial board and move states
        board_state = self.convert_flat_state_string(
            currentGame.get_board_state()
        )
        legal_moves = currentGame.get_legal_moves(True)

        return currentGame, board_state, legal_moves

    def init_eligibilities(self, board_state, legal_moves):
        # Reset all eligibilities before episode
        self.critic.reset_elegibilities()
        self.actor.reset_elegibilities()

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

    # Runs a single game using greedy on-policy strategy
    def run_game(self):
        self.actor.set_greedy()  # Makes actor fully greedy

        game = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"],
            self.game_settings["live_update_frequency"],
            True,
            f'Peg solitaire'
        )

        board_state = self.convert_flat_state_string(
            game.get_board_state()
        )
        legal_moves = game.get_legal_moves(True)

        while legal_moves:
            # Get and make the next move
            action = self.actor.get_move(board_state)
            result = game.try_move(action, return_reward=False)

            # Parse move result
            board_state, legal_moves = result
            board_state = self.convert_flat_state_string(board_state)
