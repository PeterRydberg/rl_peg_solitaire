from .Actor import Actor
from .Critic import Critic
from game.PegGame import PegGame

import itertools
import matplotlib.pyplot as plt


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
            critic_settings["c_nn_layers"],
            self.get_board_shape()
        )
        self.actor = Actor(
            actor_settings["a_learning_rate"],
            actor_settings["a_eligibility_decay"],
            actor_settings["a_discount_factor"],
            actor_settings["a_e_greediness"],
            episodes
        )

    def train_model(self):
        performance = []

        # Iterate through all episodes
        for episode in range(self.episodes):
            # Initializes the episode game
            current_game, board_state, legal_moves = self.init_game(
                display_game=(episode+1) in self.game_settings["display_game"],
                game_name=f'Episode {episode+1}'
            )

            # Initializes eligibilities at start of episode, using states
            self.init_eligibilities(board_state, legal_moves)
            actions_taken = []

            # Loops until game is lost/won
            while legal_moves:
                # Handles new board state, if actor/critic needs inits
                self.actor.handle_board_state(board_state, legal_moves)
                self.critic.handle_board_state(board_state)

                # Makes move and parses results
                prev_state, reward, board_state, legal_moves = \
                    self.make_game_choice(
                        board_state, current_game, actions_taken
                    )

                # Update critic temporal difference
                temporal_diff = self.critic.calc_temp_diff(
                    reward,
                    board_state,
                    prev_state
                )

                # Updates critic values, actor policy and eligibilities
                # for each state action pair
                self.value_policy_update(
                    actions_taken,
                    temporal_diff
                )

            self.actor.increase_greediness(self.episodes)
            performance.append(current_game.get_filled_holes())

            ##### REMOVE #####
            print(
                f'Episode {episode + 1} had performance {current_game.get_filled_holes()}'
            )

            for state, _ in actions_taken:
                value = self.critic.evaluator.get_val_from_state(state)
                print(
                    f'\tState {state} had a value of {value}')
            ##### REMOVE #####

        # Return training performance
        return performance

    # Handles updating of policy and critic values
    def value_policy_update(self, actions_taken, temporal_diff):
        self.critic.actions_update(actions_taken, temporal_diff)
        self.actor.actions_update(actions_taken, temporal_diff)

    # Make an action choice and parse the results
    def make_game_choice(self, board_state, current_game, actions_taken):
        # Get and make the next move
        prev_state = board_state
        prev_action = self.actor.get_move(board_state, training=True)
        result = current_game.try_move(prev_action, return_reward=True)

        actions_taken.append((prev_state, prev_action))

        # Parse move result
        reward, board_state, legal_moves = result
        board_state = self.convert_flat_state_string(board_state)

        return prev_state, reward, board_state, legal_moves

    # Initializes eligibilities before each episode
    def init_eligibilities(self, board_state, legal_moves):
        # Reset all eligibilities before episode
        self.critic.reset_eligibilities()
        self.actor.reset_eligibilities()

    # Converts the Peghole object state to bitstring (label)
    def convert_flat_state_string(self, board_state):
        state_string = ""
        for peghole in list(itertools.chain(*board_state)):
            if(peghole.content == "filled"):
                state_string += "1"
            elif(peghole.content == "empty"):
                state_string += "0"

        return state_string

    def display_performance_graph(self, performance):
        plt.plot(performance)
        plt.ylabel('Amount of pegs left')
        plt.xlabel('Episode number')
        plt.show()

    def get_board_shape(self):
        game = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"],
            self.game_settings["live_update_frequency"],
            False,
            None
        )
        return len(self.convert_flat_state_string(game.board.board_content))

    def init_game(
        self,
        display_game=False,
        game_name="Peg solitaire"
    ):
        # Initializes new game using game settings
        current_game = PegGame(
            self.game_settings["board_type"],
            self.game_settings["board_size"],
            self.game_settings["initial_empty"],
            self.game_settings["live_update_frequency"],
            display_game,
            game_name
        )

        # Gets initial board and move states
        board_state = self.convert_flat_state_string(
            current_game.get_board_state()
        )
        legal_moves = current_game.get_legal_moves(True)

        return current_game, board_state, legal_moves

    # Runs a single game using greedy on-policy strategy
    def run_game(self):
        self.actor.set_greedy()  # Makes actor fully greedy

        # Initializes the game
        current_game, board_state, legal_moves = self.init_game(
            True,
            'Peg solitaire'
        )

        while legal_moves:
            # Get and make the next move
            action = self.actor.get_move(board_state, legal_moves)
            result = current_game.try_move(action, return_reward=False)

            # Parse move result
            board_state, legal_moves = result
            board_state = self.convert_flat_state_string(board_state)
