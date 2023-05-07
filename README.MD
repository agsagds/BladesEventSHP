# The CTF-like mini-game

## Usage
For run the code type
``` flask --app main run --host=0.0.0.0 --port=8080```
and send ur ip to the invited users

## The legend which I used placed into `about.txt` file

## The game has two stages
1. The first stage is to get the informations about crystals place. Start path for this stage is `/rooms`
2. The second stage is to reorder and concatenate a few parts of a question, then solve it and type answer. Start path for this stage is `/swarm`. Be sure to configure ur SWARM_QUESTIONS, SWARM_ANSWERS and TEAM_SIZE in `config.py` file. TEAM_SIZE is definite which players must connect for see all parts of the question and only last connected player can see the answer input field.

