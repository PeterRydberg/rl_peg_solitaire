from ReinforcementLearner import ReinforcementLearner


def main():

    game_settings = {
        "board_type": "triangle",
        "board_size": 5,
        "initial_empty": {},
        "live_update_frequency": 2,
        "display_game": False
    }

    critic_settings = {
        "c_type": "table",
        "c_learning_rate": 0.001,
        "c_eligibility_decay": 0.05,
        "c_discount_factor": 0.05,
        "c_nn_layers": (1, 2, 3)
    }

    actor_settings = {
        "a_learning_rate": 0.1,
        "a_eligibility_decay": 0.05,
        "a_discount_factor": 0.05,
        "a_e_greediness": 0.5
    }

    try:
        rl_learner = ReinforcementLearner(
            episodes=500,
            game_settings=game_settings,
            critic_settings=critic_settings,
            actor_settings=actor_settings
        )
        print(rl_learner.actor.e_greediness)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
