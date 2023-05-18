# README

## Set-up:
1. Create the environment. You only need to do this once, but make sure to do this for each unique environment version. \
  `conda env create -f doclue_env.yml -n doclue_env`
2. List environments to make sure it has been created. \
  `conda env list` or `conda info --envs` 
3. Activate the environment. \
  `conda activate doclue_env`

![image](https://github.com/SelyanaSF/clue-less/assets/45891731/265c8421-39b7-4a37-83b2-4912630679f4)

## Run multi-player game:
Open multiple terminals
- 1 terminal for the server/splash screen
  1. To start the server, run
  `start_server.py`
  2. To exit the server, you must kill the terminal (TODO: exit by keyboard shortcut)
  
- 3-6 terminals for players
  1. To start a player terminal, run `start_client.py` for each player terminal
  2. To exit a player terminal, close out the client window

![image](https://github.com/SelyanaSF/clue-less/assets/45891731/733282d9-84bc-4341-ad8e-f4b07c7392a8)
