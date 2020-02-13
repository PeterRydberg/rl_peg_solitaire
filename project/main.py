from learner.ReinforcementLearner import ReinforcementLearner


def main():

    # See README.md for explanation of all settings

    game_settings = {
        "board_type": "triangle",
        "board_size": 6,
        "initial_empty": {},
        "live_update_frequency": 0.2,
        "display_game": (1, 50, 500)
    }

    critic_settings = {
        "c_type": "table",
        "c_learning_rate": 0.1,
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
        rl_learner.train_model()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
