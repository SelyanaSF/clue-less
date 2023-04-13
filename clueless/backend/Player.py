class Player:
    
    def __init__(self, player_name, player_id, player_current_location, player_old_location, player_hand, turn_status, player_status, player_notebook):
        # player_name : str
        # player_id : int
        # player_current_location : Tile
        # player_old_location : Tile
        # player_hand : Deck
        # turn_status : TURN_STATUS
        # player_status : PLAYER_STATUS
        # player_notebook : dict
        
        self.player_name = player_name
        self.player_id = player_id
        self.player_current_location = player_current_location
        self.player_old_location = player_old_location
        self.player_hand = player_hand
        self.turn_status = turn_status
        self.player_status = player_status
        self.player_notebook = player_notebook

    def update():
        pass

    def get_player_status():
        pass

    def set_player_status():
        pass
    
    def get_notebook():
        pass

    def get_hand():
        pass