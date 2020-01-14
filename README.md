# rl_peg_solitaire
Reinforcement learning in Python for solving the peg solitaire problem

## Activate virtual environment
Create a new environment by running `python3 -m venv ./venv`. Then activate it by running `venv\Scripts\activate.bat`. Lastly, install all dependencies by running `pip install -r requirements.txt`. Update dependencies by running `pip freeze > requirements.txt`.

## Components
The project consists of two distinct components, namely the Reinforcement Learner and the Simulated World (or environment, i.e., the game itself). This seperation is built upon the concept of the Critical Divide, where the learner does not make any assumptions about the game and the game itself does not provide any deduced (learned) information about its states. They are in seperate folders for this project.

### Reinforcement Learner (learner)


### Simulated World (game)
