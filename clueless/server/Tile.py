# custom tile class for Clue-less
# import enum

# custom class creation reference
# https://learnpython.com/blog/custom-class-python/

class Tile:

    # initialize an object of class tile
    def __init__(self, tile_name, tile_type, adjacent_tiles):
        self.tile_name = tile_name            # string name of tile
        self.tile_type = tile_type            # room, corner_room (do we need this one?), hallway
        self.is_occupied = False              # boolean that is true as long as at least one player is on the tile
        self.tile_num_players = 0             # int of number of players
        self.adjacent_tiles = adjacent_tiles  # list of string names of tiles; use dictionary in Board to access Tile objects

### GETTERS ###
    def get_tile_name(self):
        return self.tile_name

    def get_tile_type(self):
        return self.tile_type
    
    def get_tile_num_players(self):
        return self.tile_num_players
    
    def get_adjacent_tiles(self):
        return self.adjacent_tiles

# "main"
# instantiate tiles in Board class as attribute