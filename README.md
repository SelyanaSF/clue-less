# README

## Set-up:
1. Create the environment. You only need to do this once, but make sure to do this for each unique environment version. \
  `conda env create -f doclue_env.yml -n doclue_env`
2. List environments to make sure it has been created. \
  `conda env list` or `conda info --envs` 
3. Activate the environment. \
  `conda activate doclue_env`

## Run the game:
On your main directory, run `start.py` or `python3 start.py`

## Run multi-player game:
Open multiple terminals
- 1 terminal for the server/splash screen
  1. To start the server, run
  `clueless\Server.py`
  2. To exit the server, you must kill the terminal (TODO: exit by keyboard shortcut)
  
- 3-6 terminals for players
  1. To start a player terminal, run `start.py` for each player terminal
  2. To exit a player terminal, close out the client window
