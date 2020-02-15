from .CriticAnn import CriticAnn
from .CriticTable import CriticTable


class Critic:
    def __init__(
        self,
        critic_type,
        learning_rate,
        eligibility_decay,
        discount_factor,
        nn_layers
    ):
        self.critic_type = critic_type

        if(self.critic_type == "table"):
            self.evaluator = CriticTable(
                learning_rate, eligibility_decay, discount_factor
            )
        elif(self.critic_type == "ann"):
            self.evaluator = CriticAnn(
                learning_rate, eligibility_decay, discount_factor, nn_layers
            )

    # Adds new state value
    def add_state_value(self, current_state):
        self.evaluator.add_state_value(current_state)

    # Updates state value
    def update_state_value(self, state, temporal_diff):
        self.evaluator.update_state_value(state, temporal_diff)

    # Updates eligibilities
    def update_eligibilities(self, state, decay=False):
        self.evaluator.update_eligibilities(state, decay)

    # Reset all eligibilities
    def reset_eligibilities(self):
        self.evaluator.reset_eligibilities()

    # Calculates temporal difference for the new state
    def calc_temp_diff(self, reward, current_state, previous_state):
        return self.evaluator.calc_temp_diff(
            reward, current_state, previous_state
        )

    # When a new board state is introduced
    def handle_board_state(self, board_state):
        self.evaluator.handle_board_state(board_state)
