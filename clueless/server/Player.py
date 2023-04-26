class Player:
        
    def __init__(self, player_name, player_id):
        self.player_name = player_name                          # string
        self.player_id = player_id                              # int
        self.player_current_location = None                     # Tile
        self.player_old_location = None         
        self.player_hand = None                                 # Deck
        self.turn_status = 'FIRST'                              # Enum (int)
        self.player_status = 'ACTIVE'                           # Enum (int)
        # TO DO initialize dict from all tokens, weapons, room : 'unknown'
        self.player_notebook = dict()                             # Dict

    ''' GETTER FUNCTIONS '''
    # Returns the player's name
    def get_player_name(self):
        return self.player_name

    # Returns the player's iD
    def get_player_id(self):
        return self.player_id
        
    # Returns the player's status corresponding to actively playing, passively playing (lost), or unchosen
    def get_player_status(self):
        return self.player_status
    
    # Returns the player's turn status
    def get_turn_status(self):
        return self.turn_status
    
    # Returns the player's notebook
    def get_notebook(self):
        return self.player_notebook

    # Returns the player's hand, Deck of Cards
    def get_hand(self):
        return self.player_hand
 
    # Returns the player's old location
    def get_player_old_location(self):
        return self.player_old_location   
 
    # Returns the player's old location
    def get_player_current_location(self):
        return self.player_current_location    
      
    def set_player_hand(self, player_hand):
        self.player_hand= player_hand
      
    ''' SETTER FUNCTIONS '''
    # Update the player's old location and current location
    def update(self, new_location):
        self.player_old_location = self.player_current_location
        self.player_current_location = new_location
    
    # Update the player's status
    def set_player_status(self, PLAYER_STATUS):
        self.player_status = PLAYER_STATUS
    
    # Update the player's turn status
    def set_player_status(self, TURN_STATUS):
        self.turn_status = TURN_STATUS