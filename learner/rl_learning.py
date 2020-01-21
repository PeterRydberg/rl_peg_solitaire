from ReinforcementLearner import ReinforcementLearner


def main():

    try:
        rl_learner = ReinforcementLearner()
        print(rl_learner.actor)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
