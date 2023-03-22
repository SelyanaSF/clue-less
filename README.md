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

**make sure your own computer IP is in the code so that it can be run**

open multiple terminals
1 terminal for the server/splash screen
    run `clueless\Server.py`
    to exit, must kill the terminal (TODO: exit by keyboard shortcut)
3-6 terminals for players
    run `start.py` in each
    to exit, close out the client window
